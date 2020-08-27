import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

from app import create_app
from database.models import setup_db, Actor, Movie, db_drop_and_create_all
from auth.jwt_token import asssistant_jwt, director_jwt, producer_jwt


casting_assistant = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw3ejhtQko2bThTbTRHekZzV2NEViJ9.eyJpc3MiOiJodHRwczovL3Zkb2FuOTgudXMuYXV0aDAuY29tLyIsInN1YiI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nYXBpIiwiaWF0IjoxNTk4NTM4MDQ3LCJleHAiOjE1OTg2MjQ0NDcsImF6cCI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5Iiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.iQws9zRa28E4lJoE6oja5dm88K_kliL0C3C7OP_wIdpR-eWqClXXlP_Eh_CN48Xnmgjr8Q4HXGGGwywSYJj6RreAPs6cViJXR_AZUEg3OQ7WjYEANOCl-fG2HlnDRTAmc9SDwzUs6ztBpPckVc8DJwHLtH4sjnwjrOdWtxGsx-T5FsYKjZ5BWIGRFgEUS8k0nI-TihXCGHJXDWHwGG2lzkF3jSLmnUzugIaXYTeqlWrkDg0GkDKQXenRMEEssmCgG2bkfjQSTabczPROy9pf1aoRrgYoSAiqsxDo5TkqcuNOcykuhOM6Gg-YxvpNIHUijnl1vdpwGZ2CHy-AMuOmqw"

casting_director = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw3ejhtQko2bThTbTRHekZzV2NEViJ9.eyJpc3MiOiJodHRwczovL3Zkb2FuOTgudXMuYXV0aDAuY29tLyIsInN1YiI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nYXBpIiwiaWF0IjoxNTk4NTM4MzIxLCJleHAiOjE1OTg2MjQ3MjEsImF6cCI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5Iiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBkZWxldGU6YWN0b3JzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiXX0.l5Jajdllvq9Xw0mEwCCvJvoJd8GtuZOVPRVLjn3LfRXIw5F1zrpLfQXirvLJbY_8_o7oHxSl_XJGvLYi4eM94r4QkwZzP1FyNyGHp3qVwhdfSrp7zVavjOOdD1xToo5LrpTh1dP09zuZoZ_p5gEDpOkvVq9XPBIKcLGnRxHvO3KNngdeBdZTSC2DCDmlZcptGEdCi4o9Jrp_zNbxjjlR-_yLG8BjkfuCfVpk5nxN5ysVECPRevpnRy6TtHWOBj8Xt3Y0x7mkVlNoPAE2-LmHPxDLbrzXiKS-8_hGpQbzYxkZN1NX7M8ayWDJcs_TgD024gn1iXdcwuNvXQCSGyGtkQ"

casting_producer = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw3ejhtQko2bThTbTRHekZzV2NEViJ9.eyJpc3MiOiJodHRwczovL3Zkb2FuOTgudXMuYXV0aDAuY29tLyIsInN1YiI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5QGNsaWVudHMiLCJhdWQiOiJjYXN0aW5nYXBpIiwiaWF0IjoxNTk4NTM4Mzc1LCJleHAiOjE1OTg2MjQ3NzUsImF6cCI6Ik9zMkY1MXZDSDVCTEVTREw4a2l2RmpMZWh4OHVEcDZ5Iiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcG9zdDptb3ZpZXMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBkZWxldGU6YWN0b3JzIGRlbGV0ZTptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyJdfQ.JpfMhTvxPNDTVLDuJQ9irDBbDYXqxkHrps9BRCRC7T7KfEaNSiyarZIbbSpbY8ysTnH9WAfHsUqcEZzFRy6_jlF-E9s7h5d38CeP7Ps-IW-tikJtiZxX4X2-DepyOm1RrhUDubHDriESR28H2foOehnyMKN63cKm4FiMODlFJ-7yLXcXnJDwD-_sRxQO6Tre34sMRCQzsaIDvss31eknaFKC3vRghwMxYGDoIUPAatNKhV1V_FJhVrZ_XDJpgX4eqajFCyiSHZFRVAGoodtSg38pAyIE5k5GOlLbq1q2Kl26BjquPTvwp1_TyKklUEpIriNl01UMiEtEnQJtOiOKNg"

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
            "catchphrase": "I have always felt that one of the secrets of real beauty is simplicity."            
        }

        self.invalid_actor = {
            "gender": "female",
            "age": "45",
            "catchphrase": 24
        }

        self.valid_movie = {
            "title": "Gilda",
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
            "age": 35,
            "catchphrase": "If you dont have enemies, you dont have character."
        }

        self.deleted_movie = {
            "id": 2, 
            "title": "How to Marry a Millionaire",
            "year": '1953'
        }
         
        self.edited_actor = {
            "name": "Lauren Bacall",
            "gender": "female",
            "age": 27,
            "catchphrase": "Imagination is the highest kite one can fly."
        }

        self.restored_actor = {
            "name": "Lauren Bacall",
            "gender": "female",
            "age": 27,
            "catchphrase": "I am not a has-been. I am a will be."
        }

        self.edited_movie = {
            "title": "Breakfast at Tiffanys",
            "year": "1960"
        }

        self.restored_movie = {
            "id": 3,
            "title": "Breakfast at Tiffanys",
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
        res = self.client().get('/actors', headers={"Authorization": casting_assistant})
        #data = json.loads(res.data.decode('utf-8'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


        
    '''
    @DONE GET /actors/<int: actor_id>
    '''
    def test_404_get_actor_does_not_exist(self):
        res = self.client().get('/actors/2000', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
  
    '''
    @DONE GET /actors/<int: actor_id>
    '''
    def test_get_actor_detail(self):
        res = self.client().get('/actors/1', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(data['actors'])
        

    '''
    @DONE DELETE /actors/<int: actor_id>
    '''
    
    def test_delete_actor(self):
        res = self.client().delete('/actors/4', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        print(data)

        actor = Actor.query.get(4)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertEqual(actor, None)
        self.assertTrue(data['actors'])


    '''
    @DONE DELETE /actors/<int: actor_id>
    '''
    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    '''
    @DONE POST /actors
    '''
    def test_create_actor(self):
        res = self.client().post('/actors', json=self.valid_actor, headers={"Authorization": casting_producer})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    

    '''
    @DONE POST /actors
    '''
    def test_422_create_new_actor_not_allowed(self):
        res = self.client().post('/actors', json=self.invalid_actor, headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'unprocessable')


    '''
    @DONE PATCH /actors 
    '''

    def test_edit_actor(self):
        res = self.client().patch('/actors/5', json=self.edited_actor, headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    
    """
    Test Movies
    """

    '''
    @DONE GET /movies
    '''
    def test_get_movie(self):
        res = self.client().get('/movies', headers={"Authorization": casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    '''
    @DONE GET /movies/<int: movie_id>
    '''
    def test_get_movie_detail(self):
        res = self.client().get('/movies/1', headers={"Authorization": casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)
        self.assertTrue(data['movies'])


    '''
    @DONE GET /movies/<int: movie_id>
    '''
    def test_404_get_movie_does_exist(self):
        res = self.client().get('/movies/2000', headers={"Authorization": casting_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 

    
    '''
    @DONE DELETE /movies/<int: movie_id>
    '''

    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        print(data)

        movie = Movie.query.get(3)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertEqual(movie, None)


    '''
    @DONE DELETE /movies/<int: movie_id>
    '''
    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000', headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    

    '''
    @DONE POST /movies
    '''

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.valid_movie, headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])



    '''
    @DONE POST /movies
    '''
    def test_422_create_new_movie_not_allowed(self):
        res = self.client().post('/movies', json=self.invalid_movie, headers={"Authorization": casting_producer})
        data = json.loads(res.data)
        #print(data)
        #print(res.status_code)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'unprocessable')



    '''
    '''
    def test_edit_movie(self):
        res = self.client().patch('/movies/8', json=self.edited_movie, headers={"Authorization": casting_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies']) 


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


