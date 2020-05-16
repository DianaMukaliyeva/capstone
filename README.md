# Casting agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 

## Motivation

The motivation for doing this project was the opportunity to consolidate what I have learned through practice.

## Getting Started

- Base URL: [capstone-udacity](https://capstone-udacity1.herokuapp.com/)

### Authentication:

Authentication is required to communicate with api.

### Prerequisites

You need the following applications to run the server app:
1. Python 3.7*
2. Pipenv (_Optional_)

### Installation

It is preferred if you run this in a virtual environment for python. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by naviging to the cloned directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### ENVIRONMENTAL  VARIABLES

Within the cloned directore run next commands replacing with your environment variables.

```bash
export DATABASE_URL=<your_database_url>
```

#### Database Setup
```bash
createdb capstone
```

## Database Migration
for database migration, run
```
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Running the server

From within the cloned directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
In production change `FLASK_ENV` to `production`.

The application will be serve on **http://localhost:5000**

## Testing

The application uses Auth0 for authenticating users. I have created 3 test users with different roles to test the
application.

**Casting Assistant**
Username => `asisstant@assistant.com`
Password => `Assistant1`
valid_token until 17.05 19:00 => `m`

**Casting Director**
Username => `director@director.com`
Password => `Director1`
valid_token until 17.05 19:00 => `m`

**Executive Producer**
Username => `producer@producer`
Password => `Producer1`
valid_token until 17.05 19:00 => `m`

To run the tests, run
```
dropdb --if-exists capstone_test
createdb capstone_test
psql capstone_test < test_capstone.psql
python test_app.py
```

## API Documentation

#### GET '/movies'

  * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  * Request Arguments: None
  * Response: An object with a single key, categories, that contains an object of id: category_string key:value pairs. 
  * Sample:  `curl localhost:5000/categories`
```
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

#### GET '/actors'

  * Fetches the questions to be displayed on the page.
  * Request Arguments: `page`. By default value of page = 1.
  * Response: a list of question objects, a dictionary of categories, current category and total number of questions as JSON object. Results of questions are paginated in groups of 10.
  * Sample:  `curl localhost:5000/questions?page=2`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 1
}
```

#### DELETE '/movies/{question_id}'

  * Deletes the question of the given ID if it exists.
  * Request Parameters: `question_id`. ID of the existing question
  * Response: the ID of the deleted question.
  * Sample:  `curl localhost:5000/questions/22 -X DELETE`
```
{
  "deleted": 22
}
```

#### POST '/movies'

    * Search for all questions that have a given search string in the question field.
    * Returns a list of question objects, current category and total number of returned questions as JSON object.
    * Request Arguments: `searchTerm`. The search phrase.
    * Results of questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    * Sample:
         `curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "movie"}'`
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "total_questions": 1
}
```

#### POST '/questions'

    * Creates new question
    * Creates a new question using the submitted question, answer, category and difficulty. Return the ID of the created book and success value.
    * Request Arguments:
    `question` - statement of a question,
    `answer` - statement of an answer,
    `category` - ID of category,
    `difficulty` - difficulty level from 1 to 5.
    * Sample:
         ```
         curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{
             "question": "Hiiii",
             "answer": "kokokokok",
             "difficulty": "3",
             "category": "1"
         }'
         ```
```
{
  "created": 24,
  "success": true
}
```

#### GET '/categories/{category_id}/questions'

  * Fetches the questions for the requested category to be displayed on the page.
  * Request Parameters: `category_id`. The ID of the existing category.
  * Response: a list of question objects, current category and total number of questions in this category as JSON object.
  * Sample: `curl localhost:5000/categories/2/questions`
```
{
  "current_category": {
    "2": "Art"
  },
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
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

#### POST '/quizzes'

  * Fetches a random question within the given category, that is not one of the previous questions.
  * Request Arguments: 
  `previous_questions` - list of already answered questions,
  `quiz_category` - the given category object.
  * Response: the random question object as JSON object.
  * Sample:  
       ```
          curl localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{
               "previous_questions": [],
               "quiz_category": {"type":"History", "id":1}
          }'
       ```
```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}
```

## Error Handling

This application uses convential HTTP response codes to indicate a success or a failure.
Errors are returned as JSON objects in the following format:

```
{
    'success': True
    'error': 400,
    'message': 'bad request'
}
```

The API return next error types when request fails:

* 400: Bad Request
* 401: Unauthorized
* 404: Resource Not Found
* 422: Not Processable
* 500: Something went wrong!



## Authors

**Diana Mukaliyeva** - [DianaMukaliyeva](https://github.com/DianaMukaliyeva)

## License

This project is licensed under the MIT license.

## Acknowledgments

* [Udacity](https://www.udacity.com/)
* [Auth0](https://auth0.com/)

