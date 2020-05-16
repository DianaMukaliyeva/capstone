import os

from flask import (
    Flask,
    request,
    abort,
    jsonify,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from auth0 import AuthError, requires_auth
from models import setup_db, Movie, Actor


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        """Intercept response to add 'Access-Control-Allow' headers"""

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        '''Redirecting to login page'''

        return redirect('https://capstone-udacity.eu.auth0.com/authorize?response_type=token\
            &client_id=8V0Rt7JzfDgHBnHXd5gWJ1uMxkfnFu1l\
            &redirect_uri={}'.format(os.getenv('REDIRECT_URI')))

    # Movies
    # ---------------------------------------------------------

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        '''Get all movies from database

        Returns in json format
        ----------------------
        movies: list of movies (id, title and release date)
        '''

        movies = Movie.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_actors_in_movie(jwt, movie_id):
        '''Get list of assigned actors for the movie with given id

        Parameters
        ----------
        movie_id: integer representing the movie

        Returns in json format
        ----------------------
        title: movie's title
        actors: list of actors in selected movie
        '''

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            return jsonify({
                'success': True,
                'title': movie.title,
                'actors': [actor.format() for actor in movie.actors]
            })
        except Exception:
            abort(400)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        '''Add a movie to database

        Arguments in json format
        ------------------------
        title: name of movie to be created
        release_date: release date of movie to be created

        Returns json object
        -------------------
        movie: movie's id, title and release date
        '''

        data = request.get_json()
        try:
            movie = Movie(title=data.get('title'),
                          release_date=data.get('release_date'))
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        '''Modify a movie with given id

        Arguments in json format
        ------------------------
        title: name of movie, optional
        release_date: release date of movie, optional
        actors: list of actors ids assigned to the movie,
                list of integers, optional

        Parameters
        ----------
        movie_id: integer representing the movie to be updated

        Returns json object
        -------------------
        movie: movie's id, title and release date
        '''

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            data = request.get_json()
            if 'title' in data:
                movie.title = data.get('title')
            if 'release_date' in data:
                movie.release_date = data.get('release_date')
            if 'actors' in data:
                actors = data.get('actors')
                movie.actors = []
                for actor_id in actors:
                    actor = Actor.query.filter_by(id=actor_id).one_or_none()
                    if actor is None:
                        raise Exception
                    movie.actors.append(actor)
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        '''Delete a movie from database

        Parameters
        ----------
        movie_id: integer representing the movie to be deleted

        Returns json object
        -------------------
        deleted: deleted movie
        '''

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.format()
            })
        except Exception:
            abort(422)

    # Actors
    # --------------------------------------------------------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        '''Get all actors from database

        Returns in json format
        ----------------------
        actors: list of actors (id, name, age and gender)
        '''

        actors = Actor.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_movies_from_actor(jwt, actor_id):
        '''Get a list of movies where the actor is assigned

        Parameters
        ----------
        actor_id: integer representing the actor

        Returns in json format
        ----------------------
        actor: actor
        movies: list of movies
        '''

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            return jsonify({
                'success': True,
                'actor': actor.format(),
                'movies': [movie.format() for movie in actor.movies]
            })
        except Exception:
            abort(400)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        '''Add an actor to database

        Arguments in json format
        ------------------------
        name: name of actor to be added, string
        age: actor's age, integer
        gender: actor's gender (male, female or other), string

        Returns json object
        -------------------
        actor: actor's id, name, age and gender
        '''

        data = request.get_json()
        try:
            gender = data.get('gender').lower()
            if gender not in ['male', 'female', 'other']:
                raise Exception
            actor = Actor(
                name=data.get('name'),
                age=data.get('age'),
                gender=gender
            )
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        '''Modify an actor with given id

        Arguments in json format
        ------------------------
        name: name of actor, string, optional
        age: age of actor, integer, optional
        gender: actor's gender, string (male, female or other), optional
        movies: list of movies ids to which actor is assigned,
                list of integers, optional

        Parameters
        ----------
        actor_id: integer representing the actor to be updated

        Returns json object
        -------------------
        actor: actor's id, name, age and gender
        '''

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            data = request.get_json()
            if 'name' in data:
                actor.name = data.get('name')
            if 'age' in data:
                actor.age = data.get('age')
            if 'gender' in data:
                gender = data.get('gender').lower()
                if gender not in ['male', 'female', 'other']:
                    raise Exception
                actor.gender = gender
            if 'movies' in data:
                movies = data.get('movies')
                actor.movies = []
                for movie_id in movies:
                    movie = Movie.query.filter_by(id=movie_id).one_or_none()
                    if movie is None:
                        raise Exception
                    actor.movies.append(movie)
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        '''Delete an actor from database

        Parameters
        ----------
        actor_id: integer representing the actor to be deleted

        Returns json object
        -------------------
        delete: deleted actor
        '''

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor.format()
            })
        except Exception:
            abort(422)

    # Error handling
    # ------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        '''Error handler for 400'''

        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        '''Error handler for 404'''

        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        '''Error handler for 422'''

        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    # @app.errorhandler(Exception)
    # def internal_error(error):
    #     '''Generic error handler for all exceptions'''

    #     return jsonify({
    #         'success': False,
    #         'error': 500,
    #         'message': 'Something went wrong!'
    #     }), 500

    @app.errorhandler(AuthError)
    def authorization_error(error):
        '''Generic error handler for all exceptions'''

        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run()
