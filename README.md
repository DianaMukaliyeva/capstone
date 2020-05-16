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

##### Environmental variables

Within the cloned directore run next commands replacing `DATABASE_URL` with your information.

```bash
source setup.sh
```

#### Database Setup

Create database and for database  migration, run

```bash
createdb capstone
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

- Username => `asisstant@assistant.com`
- Password => `Assistant1`
- Permission => Can view actors and movies
- valid_token until 17.05 19:00 => in `setup.sh` file

**Casting Director**

- Username => `director@director.com`
- Password => `Director1`
- Permission => Can view actors and movies. Add or delete an actor from the database. Modify actors or movies.
- valid_token until 17.05 19:00 => in `setup.sh` file

**Executive Producer**

- Username => `producer@producer`
- Password => `Producer1`
- Permission => Can view actors and movies.  Add or delete an actor from the database. Modify actors or movies. Add or delete a movie from the database.
- valid_token until 17.05 19:00 => in `setup.sh` file

To run the tests, run
```
dropdb --if-exists capstone_test
createdb capstone_test
psql capstone_test < test_capstone.psql
python test_app.py
```
And do not forget to `source setup.sh` to export tokens (if necessary replace with valid tokens).

## API Documentation

#### GET '/movies'

  * Fetches a list of movies.
  * Request Arguments: None.
  * Response: A list of movies (id, title and release date).
  * Sample: 
        ```
        curl 'https://capstone-udacity1.herokuapp.com/movies' --header 'Authorization: Bearer <token>'
        ```
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Sunday, Jul 25 2021",
            "title": "New Movie soon"
        }
    ],
    "success": true
}
```

#### GET '/actors'

  * Fetches a list of actors.
  * Request Arguments: None.
  * Response: A list of actors (id, name, age and gender).
  * Sample: 
        ```
        curl 'https://capstone-udacity1.herokuapp.com/actors' --header 'Authorization: Bearer <token>'
        ```
```
{
    "actors": [
        {
            "age": 55,
            "gender": "male",
            "id": 1,
            "name": "John Smith"
        }
    ],
    "success": true
}
```

#### GET '/movies/{movie_id}'

  * Fetches the list of assigned actors for the movie with given id.
  * Request Parameters: `movie_id`. ID of the existing movie
  * Response:  movie's title and list of actors in selected movie.
  * Sample: 
        ```
        curl 'https://capstone-udacity1.herokuapp.com/movies/1' --header 'Authorization: Bearer <token>'
        ```
```
{
    "actors": [
        {
            "age": 55,
            "gender": "male",
            "id": 4,
            "name": "John Smith"
        },
        {
            "age": 55,
            "gender": "male",
            "id": 5,
            "name": "John Smith"
        }
    ],
    "success": true,
    "title": "Movie with ID 1"
}
```

#### GET '/actors/{actor_id}'

  * Fetches the list of movies where the actor is assigned.
  * Request Parameters: `actor_id`. ID of the existing actor.
  * Response: an actor and list of movies.
  * Sample: 
        ```
        curl 'https://capstone-udacity1.herokuapp.com/actors/1' --header 'Authorization: Bearer <token>'
        ```
```
{
    "actor": {
        "age": 55,
        "gender": "female",
        "id": 1,
        "name": "new name"
    },
    "movies": [],
    "success": true
}
```

#### DELETE '/movies/{movie_id}'

  * Deletes the movie of the given ID if it exists.
  * Request Parameters: `movie_id`. ID of the existing movie.
  * Response: deleted movie.
  * Sample: 
        ```
        curl -X DELETE 'https://capstone-udacity1.herokuapp.com/movies/5' --header 'Authorization: Bearer <token>'
        ```
```
{
    "deleted": {
        "id": 5,
        "release_date": "Sunday, Jul 25 2021",
        "title": "New Movie soon"
    },
    "success": true
}
```

#### DELETE '/actors/{actor_id}'

  * Deletes the actor of the given ID if it exists.
  * Request Parameters: `actor_id`. ID of the existing actor
  * Response: The deleted actor.
  * Sample: 
        ```
        curl -X DELETE 'https://capstone-udacity1.herokuapp.com/actors/5' --header 'Authorization: Bearer <token>'
        ```
```
{
    "deleted": {
        "age": 55,
        "gender": "male",
        "id": 5,
        "name": "John Smith"
    },
    "success": true
}
```

#### POST '/movies'

  * Add a movie to database.
  * Request Arguments: `title`, `release_date`. `Release_date` should represent date.
  * Returns a movie's id, title and release date.
  * Sample: 
        ```
        curl -X POST 'https://capstone-udacity1.herokuapp.com/movies/5' --header 'Authorization: Bearer <token>' --header "Content-Type: application/json" -d '{"title": "New Movie soon", "release_date": "07-25-2021"}'
        ```
```
{
    "movie": {
        "id": 5,
        "release_date": "Sunday, Jul 25 2021",
        "title": "New Movie soon"
    },
    "success": true
}
```

#### POST '/actors'

  * Add an actor to database.
  * Request Arguments: `name`, `age` and `gender`. `Gender` should be `male`, `female` or `other`. `Age` as a Integer.
  * Returns an actor's id, name, age and gender.
  * Sample: 
        ```
        curl -X POST 'https://capstone-udacity1.herokuapp.com/actors/6' --header 'Authorization: Bearer <token>' --header "Content-Type: application/json" -d '{"name": "John Smith", "age": 55, "gender": "male"}'
        ```
```
{
    "actor": {
        "age": 55,
        "gender": "male",
        "id": 6,
        "name": "John Smith"
    },
    "success": true
}
```

#### PATCH '/movies/{movie_id}'

  * Modify a movie with given id.
  * Request Arguments:
`title` - name of movie, optional,
`release_date` - release date of movie, optional,
`actors` - list of actors ids assigned to the movie, list of integers, optional.
  * Sample: 
        ```
        curl -X PATCH 'https://capstone-udacity1.herokuapp.com/movies/1' --header 'Authorization: Bearer <token>' --header "Content-Type: application/json" -d '{"title": "77777", "actors": [4, 5]}'
        ```
```
{
    "movie": {
        "id": 1,
        "release_date": "Saturday, Apr 16 2022",
        "title": "77777"
    },
    "success": true
}
```

#### PATCH '/actors/{actor_id}'

  * Modify an actor with given id.
  * Request Arguments:
`name` - name of actor, string, optional,
`age` - age of actor, integer, optional,
`gender` - actor's gender, string (male, female or other), optional,
`actors` - list of movies ids to which actor is assigned, list of integers, optional.
  * Sample: 
        ```
        curl -X PATCH 'https://capstone-udacity1.herokuapp.com/actors/1' --header 'Authorization: Bearer <token>' --header "Content-Type: application/json" -d '{"name": "new name", "gender": "female"}'
        ```
```
{
    "actor": {
        "age": 55,
        "gender": "female",
        "id": 1,
        "name": "new name"
    },
    "success": true
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

