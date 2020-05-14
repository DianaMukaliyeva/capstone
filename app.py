from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

app = Flask(__name__)
CORS(app)
setup_db(app)

@app.route('/')
def index():
    return 'Hello there\n'

@app.route('/movies')
def show_movies():
    movies = Movie.query.all()
    response = [movie.format() for movie in movies]
    return jsonify({
        'movies': response
    })


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8080)

