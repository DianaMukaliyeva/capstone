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

    # @app.route('/movies/<int:movie_id>/actors')
    # def get_actors_in_movie(movie_id):
    #     '''Get list of assigned actors for the movie with given id

    #     Parameters
    #     ----------
    #     movie_id: integer representing the movie

    #     Returns in json format
    #     ----------------------
    #     movie: movie's id, title and release date
    #     actors: list of actors in selected movie
    #     '''
    #     pass

    # @app.route('/movies/', methods=['POST'])
    # def create_movie():
    #     '''Add a movie to database

    #     Arguments in json format
    #     ------------------------
    #     title: name of movie to be created
    #     release_date: release date of movie to be created

    #     Returns json object
    #     -------------------
    #     movie: movie's id, title and release date
    #     '''
    #     pass

    # @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    # def update_movie(movie_id):
    #     '''Modify a movie with given id

    #     Arguments in json format
    #     ------------------------
    #     title: name of movie, optional
    #     release_date: release date of movie, optional

    #     Parameters
    #     ----------
    #     movie_id: integer representing the movie to be updated

    #     Returns json object
    #     -------------------
    #     movie: movie's id, title and release date
    #     '''
    #     pass

    # @app.route('/movies/<int:movie_id>', method=['DELETE'])
    # def delete_movie(movie_id):
    #     '''Delete a movie from database

    #     Parameters
    #     ----------
    #     movie_id: integer representing the movie to be deleted

    #     Returns json object
    #     -------------------
    #     delete: deleted movie's id and title
    #     '''
    #     pass

    # # Actors
    # # --------------------------------------------------------

    # @app.route('/actors')
    # def get_actors():
    #     '''Get all actors from database

    #     Returns in json format
    #     ----------------------
    #     actors: list of actors (id, name, age and gender)
    #     '''

    #     actors = Actor.query.all()
    #     return jsonify({
    #         'status': True,
    #         'actors': [actor.format() for actor in actors]
    #     })

    # @app.route('/actors/<int:actor_id>/movies')
    # def get_movies_from_actor(actor_id):
    #     '''Get a list of movies where the actor is assigned

    #     Parameters
    #     ----------
    #     actor_id: integer representing the actor

    #     Returns in json format
    #     ----------------------
    #     actor: actor's id, name
    #     movies: list of movies
    #     '''
    #     pass

    # @app.route('/actors/', methods=['POST'])
    # def create_actor():
    #     '''Add an actor to database

    #     Arguments in json format
    #     ------------------------
    #     name: name of actor to be added, string
    #     age: actor's age, integer
    #     gender: actor's gender (male, female or other), string

    #     Returns json object
    #     -------------------
    #     actor: actor's id, name, age and gender
    #     '''
    #     pass

    # @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    # def update_actor(actor_id):
    #     '''Modify an actor with given id

    #     Arguments in json format
    #     ------------------------
    #     name: name of actor, string, optional
    #     age: age of actor, integer, optional
    #     gender: actor's gender, string (male, female or other), optional

    #     Parameters
    #     ----------
    #     actor_id: integer representing the actor to be updated

    #     Returns json object
    #     -------------------
    #     actor: actor's id, name, age and gender
    #     '''
    #     pass

    # @app.route('/actors/<int:actor_id>', method=['DELETE'])
    # def delete_actor(actor_id):
    #     '''Delete an actor from database

    #     Parameters
    #     ----------
    #     actor_id: integer representing the actor to be deleted

    #     Returns json object
    #     -------------------
    #     delete: deleted actor's id and name
    #     '''
    #     pass

    return app
