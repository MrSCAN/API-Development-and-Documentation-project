# API Documentation [Author @MrScan]

## Base Url `http://127.0.0.1:5000`

## Edpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

### Example:

- **Request** `curl -X GET http://127.0.0.1:5000/categories`

- **Response:**

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

### Example:

- **Request** `curl -X GET http://127.0.0.1:5000/questions?page=2`

- **Response:**

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {},
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "total_questions": 19
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

### Example:

- **Request** `curl -X GET http://127.0.0.1:5000/categories/2/questions`

- **Response:**

```json
{
  "current_category": {
    "id": 2,
    "type": "Art"
  },
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}
```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: An object with keys; `deleted` the `id` of the deleted question and `succes` flag set to `True`.

### Example:

- **Request** `curl -X DELETE http://127.0.0.1:5000/categories/5`

- **Response:**

```json
{
  "deleted": 5,
  "success": true
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body: `{"question": "Who is the prince of Africa","answer": "MrScan","difficulty": 1,"category": 1}` The `question`, `answer`, `difficulty` and `category` encoded as json string.
- Returns: An object with keys; `created` the `id` of the created question and `succes` flag set to `True`.

### Example:

- **In Postman, make a post Request to** `curl -X DELETE http://127.0.0.1:5000/categories` **using `{"question": "Who is the prince of Africa","answer": "MrScan","difficulty": 1,"category": 1}` as request body**

- **Response:**

```json
{
  "created": 38,
  "success": true
}
```

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "the prince of Africa"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": {},
  "questions": [
    {
      "answer": "MrScan",
      "category": 1,
      "difficulty": 1,
      "id": 38,
      "question": "Who is the prince of Africa"
    }
  ],
  "total_questions": 1
}
```

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{ "previous_questions": [3, 19], "quiz_category": { "type": "Art", "id": 2 } }
```

- Returns: a single new question object

```json
{
  "question": {
    "answer": "One",
    "category": 2,
    "difficulty": 4,
    "id": 18,
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }
}
```
