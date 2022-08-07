from dataclasses import dataclass
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME, DB_USER, DB_PASSWORD

"""To deploy the tests, run from backend folder;

bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
"""


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format(
        DB_USER, DB_PASSWORD, "localhost:5432", TEST_DB_NAME
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Who is the prince of Africa","answer": "MrScan","difficulty": 1,"category": 1}
        self.valid_quizz_json = {"previous_questions": [], "quiz_category": {"type": "Art", "id": 2}}
        self.invalid_quizz_json = {"previous_questions": [], "quiz_category": {"type": "Hello", "id": 200}}
        self.questions_in_db = 19
        self.number_of_categories = 6

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["total_questions"], self.questions_in_db)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["categories"]), self.number_of_categories)
        self.assertTrue(data["categories"])

    def test_405_for_invalid_methods_for_categories(self):
        res = self.client().post("/categories", json={'id': 2, 'type': 'City'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_create_new_questions(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    def test_delete_question(self):
        created_item = Question.query.order_by(Question.id.desc()).first().id
        res = self.client().delete("/questions/"+str(created_item))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == created_item).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], created_item)
        self.assertEqual(question, None)

    def test_404_if_you_try_to_delete_question_that_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 2)

    def test_404_for_questions_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "kyrgsvgdhsvshb"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_retrieve_questions_with_category_id(self):
        res = self.client().get("/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_category"], {'id': 2, 'type': 'Art'} )
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 4)

    def test_422_for_retrieve_questions_with_invalid_category_id(self):
        res = self.client().get("/categories/2077/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_quizz_question_with_valid_payload(self):
        res = self.client().post("/quizzes", json=self.valid_quizz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_422_get_quizz_question_with_invalid_payload(self):
        res = self.client().post("/quizzes", json=self.invalid_quizz_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()