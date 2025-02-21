from ast import Pass
import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    # CORS(app, resources={r"*/api/*" : {'origins': '*'}})
    CORS(app)


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTION"
        )
        return response


    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_question = questions[start:end]

        return current_question

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def fetch_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            response = {}
            if len(categories) == 0:
                abort(404)
            for category in categories:
                response[category.id] = category.type
            return jsonify(
                {
                    "categories":response
                }
            )
        except:
            abort(400)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        categories = Category.query.order_by(Category.id).all()
        response = {}
        if len(categories) == 0:
            abort(404)
        for category in categories:
            response[category.id] = category.type
        return jsonify(
            {
                "questions": current_questions,
                "total_questions": len(selection),
                "categories": response,
                "current_category": {}
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        question.delete()
        return jsonify(
            {
                "success": True,
                "deleted": question_id
            }
        )


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

    ANSWER: Added to get questions module
    """
    @app.route("/questions", methods=["POST"])
    def add_questions():
        body = request.get_json()
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        searchTerm = body.get("searchTerm", None)
        if searchTerm:
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(searchTerm))).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)
            categories = Category.query.order_by(Category.id).all()
            response = {}
            if len(categories) == 0:
                abort(404)
            for category in categories:
                response[category.id] = category.type
            return jsonify(
                {
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "categories": response,
                    "current_category": {}
                })
        else:
            question = Question(question, answer, category, difficulty)
            question.insert()
            return jsonify(
            {
                "success": True,
                "created": question.id
            })   


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.

    Completed Above
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def retrieve_questions_category_id(category_id):
        try:
            selection = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)
            category = Category.query.get(category_id)
            if not category:
                abort(404)
            return jsonify(
                {
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "current_category": category.format()
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # {previous_questions: [], quiz_category: {type: "click", id: 0}}
    @app.route("/quizzes", methods=["POST"])
    def get_quizz_question():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            category_id = body.get("quiz_category", None)['id']
            if category_id == 0:
                questions = Question.query.order_by(Question.id).all()
            else:
                questions = Question.query.filter(Question.category==category_id).order_by(Question.id).all()
            #Check if questions were returned
            if len(questions) == 0:
                abort(404)
            unseen_questions = [question for question in questions if question.id not in previous_questions ]
            if len(unseen_questions) == 0:
                return jsonify({"question":None})
            question = random.choice(unseen_questions)
            
            return jsonify({"question":question.format()})
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

