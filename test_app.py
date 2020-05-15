import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from database.models import setup_db, Actor, Movie
from app import create_app


class CapstoneTestCase(unittest.TestCase):
    '''This class represents the Capstone project test cases'''

    def setUp(self):
        '''Define test variables and initialize app.'''

        self.app = create_app()
        self.client = self.app.test_client
        self.db_name = 'capstone_test'
        self.database_path = \
            f'postgres://postgres:postgres@localhost:5432/{self.db_name}'
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


'''Make the tests conveniently executable'''
if __name__ == "__main__":
    unittest.main()
