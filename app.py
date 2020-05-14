from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

app = Flask(__name__)
CORS(app)
setup_db(app)

@app.route('/')
def index():
    return 'Hello there\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

