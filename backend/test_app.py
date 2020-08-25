import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 

from app import create_app
from database.models import setup_db, Actor, Movie 

class CastingTestCase(unittest.TestCase):
    """This class represents the casting app test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app() 
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'DataPass98','localhost:5432', 'castingagency')
        setup_db(self.app, self.database_path)

        self.valid_actor = {
            "name" : "Rita Hayworth",
            "gender" : "female",
            "age": 24, 
            "imagelink": "https://www.biography.com/.image/c_fill%2Ccs_srgb%2Cfl_progressive%2Ch_400%2Cq_auto:good%2Cw_620/MTIwNjA4NjMzODM3NjE4NzAw/rita-hayworth-9332633-1-402.jpg",
            "catchphrase": "I have always felt that one of the secrets of real beauty is simplicity."            
        }

        self.invalid_actor = {
            "gender": "female",
            "age": "45",
            "catchphrase": 24
        }

        self.valid_movie = {
            "title": "Gilda",
            "imagelink": "https://upload.wikimedia.org/wikipedia/commons/1/15/Gilda_%281946_one-sheet_poster_-_Style_B%29.jpg",
            "year": '1946'
        }

        self.invalid_movie = {
            "title": "Gilda",
            "year": 1946
        }

        self.deleted_actor = {
            "id": 4,
            "name": "Paul Newman",
            "gender": "male",
            "age": "35",
            "imagelink": "https://s3.amazonaws.com/images.hamlethub.com/hh20mediafolder/942/201807/frases-newman_0-1532976269.JPG",
            "catchphrase": "If you dont have enemies, you dont have character."
        }

        self.deleted_movie = {
            "id": 2, 
            "title": "How to Marry a Millionaire",
            "imagelink": "https://www.amanandamouse.com/blogspot/marrymillionaire.jpg",
            "year": '1953'
        }
         
        self.edited_actor = {
            "name": "Lauren Bacall",
            "gender": "female",
            "age": 27,
            "imagelink": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Lauren_Bacall_1945_%28cropped%29.jpg",
            "catchphrase": "Imagination is the highest kite one can fly."
        }

        self.restored_actor = {
            "name": "Lauren Bacall",
            "gender": "female",
            "age": 27,
            "imagelink": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Lauren_Bacall_1945_%28cropped%29.jpg",
            "catchphrase": "I am not a has-been. I am a will be."
        }

        self.edited_movie = {
            "id": 3,
            "title": "Breakfast at Tiffanys",
            "imagelink": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Breakfast_at_Tiffany%27s_%281961_poster%29.jpg/1200px-Breakfast_at_Tiffany%27s_%281961_poster%29.jpg",
            "year": '1960'
        }

        self.restored_movie = {
            "id": 3,
            "title": "Breakfast at Tiffanys",
            "imagelink": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Breakfast_at_Tiffany%27s_%281961_poster%29.jpg/1200px-Breakfast_at_Tiffany%27s_%281961_poster%29.jpg",
            "year": '1961'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        #self.client().post('/actors', json=self.deleted_actor)
        #self.client().post('/movies', json=self.deleted_movie)

    """
    Test Actor
    """

    '''
    @DONE GET /actors test 
    '''
    def test_get_actor(self):
        res = self.client().get('/actors')
        #data = json.loads(res.data.decode('utf-8'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        

    '''
    @DONE GET /actors/<int: actor_id>
    '''
    def test_404_get_actor_does_not_exist(self):
        res = self.client().get('/actors/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
       
    '''
    @DONE GET /actors/<int: actor_id>
    '''
    def test_get_actor_detail(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(data['actors'])

    
    '''
    @DONE DELETE /actors/<int: actor_id>
    '''
    def test_delete_actor(self):
        res = self.client().delete('/actors/4')
        data = json.loads(res.data)

        actor = Actor.query.get(4)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertEqual(question, None)
        self.assertTrue(len(data['actors']))


    '''
    @DONE DELETE /actors/<int: actor_id>
    '''
    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    '''
    @DONE POST /actors
    '''
    def test_create_actor(self):
        res = self.client().post('/actors', json=self.valid_actor)
        data = json.loads(res.data)
        print(data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    def test_422_create_new_actor_not_allowed(self):
        res = self.client().post('/actors', json=self.invalid_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'unprocessable')


    def test_edit_actor(self):
        res = self.client().patch('/actors/5', self.edited_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    
    def test_404_edit_actor_does_not_exist(self):
        res = self.client().patch('/actors/20000', self.edited_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    
    """
    Test Movies
    """

    '''
    @DONE GET /movies
    '''
    def test_get_movie(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    '''
    @DONE GET /movies/<int: movie_id>
    '''
    def test_get_movie_detail(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(data['movies'])


    '''
    @DONE GET /movies/<int: movie_id>
    '''
    def test_404_get_movie_does_exist(self):
        res = self.client().get('/movies/2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 

    
    '''
    @DONE DELETE /movies/<int: movie_id>
    '''
    def test_delete_movie(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        movie = Movie.query.get(2)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(question, None)
        self.assertTrue(data['movies'])


    '''
    @DONE DELETE /movies/<int: movie_id>
    '''
    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    '''
    @DONE POST /movies
    '''
    def test_create_movie(self):
        res = self.client().post('/movies', json=self.valid_movie)
        data = json.loads(res.data)
        print(data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_422_create_new_movie_not_allowed(self):
        res = self.client().post('/movies', json=self.invalid_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'unprocessable')


    def test_edit_movie(self):
        res = self.client().patch('/movies/3', self.edited_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors'])) 

    
    def test_404_edit_movie_does_not_exist(self):
        res = self.client().patch('/movies/3', self.edited_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


