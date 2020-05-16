import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie
from app import create_app


assistant_header = {"Authorization":
                    "Bearer {}".format(os.getenv('ASSISTANT_TOKEN'))}
director_header = {"Authorization":
                   "Bearer {}".format(os.getenv('DIRECTOR_TOKEN'))}
producer_header = {"Authorization":
                   "Bearer {}".format(os.getenv('PRODUCER_TOKEN'))}


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

        self.new_actor = {
            'name': 'Test Name',
            'age': 35,
            'gender': 'male'
        }
        self.new_movie = {
            'title': 'Test movie',
            'release_date': '12-12-2012'
        }

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # CASTING ASSISTANT TESTING

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_specific_movie_casting_assistant(self):
        res = self.client().get('/movies/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_specific_actor_casting_assistant(self):
        res = self.client().get('/actors/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_nonexisting_movie_casting_assistant_404(self):
        res = self.client().get('/movies/100', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_nonexisting_actor_casting_assistant_404(self):
        res = self.client().get('/actors/100', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_movies_casting_assistant_401(self):
        res = self.client().post(
            '/movies',
            headers=assistant_header,
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_actors_casting_assistant_401(self):
        res = self.client().post(
            '/actors',
            headers=assistant_header,
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_movies_casting_assistant_401(self):
        res = self.client().patch(
            '/movies/1',
            headers=assistant_header,
            json={'release_date': '21-12-2012'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_actors_casting_assistant_401(self):
        res = self.client().patch(
            '/actors/1',
            headers=assistant_header,
            json={'age': 53}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movies_casting_assistant_401(self):
        res = self.client().delete('/movies/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actors_casting_assistant_401(self):
        res = self.client().delete('/actors/1', headers=assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # CASTING DIRECTOR TESTING

    def test_get_movies_casting_director(self):
        res = self.client().get('/movies', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_casting_director_401(self):
        res = self.client().post(
            '/movies',
            headers=director_header,
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_post_actors_casting_director(self):
        res = self.client().post(
            '/actors',
            headers=director_header,
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_casting_director(self):
        res = self.client().patch(
            '/movies/1',
            headers=director_header,
            json={'release_date': '02-12-2012'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_casting_director(self):
        res = self.client().patch(
            '/actors/1',
            headers=director_header,
            json={'age': 53}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_casting_director_401(self):
        res = self.client().delete('/movies/2', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actors_casting_director(self):
        res = self.client().delete('/actors/2', headers=director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # EXECUTIVE PRODUCER TESTING

    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_executive_producer(self):
        res = self.client().post(
            '/movies',
            headers=producer_header,
            json=self.new_movie
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_actors_executive_producer(self):
        res = self.client().post(
            '/actors',
            headers=producer_header,
            json=self.new_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_executive_producer(self):
        res = self.client().patch(
            '/movies/1',
            headers=producer_header,
            json={'release_date': '03-12-2012'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_executive_producer(self):
        res = self.client().patch(
            '/actors/1',
            headers=producer_header,
            json={'age': 53}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/3', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/3', headers=producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


'''Make the tests conveniently executable'''
if __name__ == "__main__":
    unittest.main()
