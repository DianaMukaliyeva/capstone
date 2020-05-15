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

from models import setup_db, Movie, Actor


def create_app():
    '''Creates and sets up a Flask application

    Returns
    -------
    Flask application
    '''

    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Hello there! You are about to sign in to Casting agency.\n'

    # Movies
    # ---------------------------------------------------------

    @app.route('/movies')
    def get_movies():
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

    @app.route('/movies/<int:movie_id>/actors')
    def get_actors_in_movie(movie_id):
        '''Get list of assigned actors for the movie with given id

        Parameters
        ----------
        movie_id: integer representing the movie

        Returns in json format
        ----------------------
        movie: movie's id, title and release date
        actors: list of actors in selected movie
        '''

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            return jsonify({
                'movie': movie.format(),
                'actors': [actor.format() for actor in movie.actors]
            })
        except Exception:
            abort(400)

    @app.route('/movies', methods=['POST'])
    def create_movie():
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
    def update_movie(movie_id):
        '''Modify a movie with given id

        Arguments in json format
        ------------------------
        title: name of movie, optional
        release_date: release date of movie, optional

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
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        '''Delete a movie from database

        Parameters
        ----------
        movie_id: integer representing the movie to be deleted

        Returns json object
        -------------------
        deleted: deleted movie's id and title
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
    def get_actors():
        '''Get all actors from database

        Returns in json format
        ----------------------
        actors: list of actors (id, name, age and gender)
        '''

        actors = Actor.query.all()
        return jsonify({
            'status': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<int:actor_id>/movies')
    def get_movies_from_actor(actor_id):
        '''Get a list of movies where the actor is assigned

        Parameters
        ----------
        actor_id: integer representing the actor

        Returns in json format
        ----------------------
        actor: actor's id, name
        movies: list of movies
        '''

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            return jsonify({
                'actor': actor.format(),
                'movies': [movie.format() for movie in actor.movies]
            })
        except Exception:
            abort(400)

    @app.route('/actors', methods=['POST'])
    def create_actor():
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
    def update_actor(actor_id):
        '''Modify an actor with given id

        Arguments in json format
        ------------------------
        name: name of actor, string, optional
        age: age of actor, integer, optional
        gender: actor's gender, string (male, female or other), optional

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
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        '''Delete an actor from database

        Parameters
        ----------
        actor_id: integer representing the actor to be deleted

        Returns json object
        -------------------
        delete: deleted actor's id and name
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

    @app.errorhandler(Exception)
    def internal_error(error):
        '''Generic error handler for all exceptions'''

        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Something went wrong!'
        }), 500

    return app
