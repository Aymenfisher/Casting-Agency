import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movies,Actors,setup_db


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        #tokens for getting access:
        self.casting_assistant=os.environ['casting_assistant']
        self.casting_director=os.environ['casting_director']
        self.executive_producer=os.environ['executive_producer']
        self.new_actor={'name':'steven seagal',
        'age':69,
        'gender':'male'
        }
        self.new_movie={'title':'Tinker Tailor Soldier Spy',
        'release_date':'2011-09-16'
        }

        self.app.app_context().push()

    
    def tearDown(self):
        """Executed after reach test"""
        pass



    ################ RBAC TESTS #############

    #Casting assistant tests:
    def test_casting_assistant_allowed_actions(self):
        '''tests the allowed actions fot the casting assistant role '''
        get_actors=self.client().get('/actors',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        get_movies=self.client().get('/movies',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})

        self.assertEqual(get_actors.status_code,200)
        self.assertEqual(get_movies.status_code,200)
    
    
    def test_forbidden_actions_casting_assistant(self):
        ''' tests all the forbidden endpoints for the casting assistant role'''
        post_actor=self.client().post('/actors',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        post_movie=self.client().post('/movies',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        delete_actor=self.client().delete('/actors/6',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        delete_movie=self.client().delete('/movies/6',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        patch_actor=self.client().patch('/actors/1',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})
        patch_movie=self.client().patch('/movies/1',headers={'Authorization':"Bearer {}".format(self.casting_assistant)})

        self.assertEqual(post_actor.status_code,403)
        self.assertEqual(post_movie.status_code,403)
        self.assertEqual(delete_actor.status_code,403)
        self.assertEqual(delete_movie.status_code,403)
        self.assertEqual(patch_actor.status_code,403)
        self.assertEqual(patch_movie.status_code,403)
    
    # Casting Director tests :
    def test_casting_director_allowed_actions(self):
        ''' tests the allowed actions for the casting assistant role'''
        get_actors=self.client().get('/actors',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        get_movies=self.client().get('/movies',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        post_actor=self.client().post('/actors',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        delete_actor=self.client().delete('/actors/6',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        patch_actor=self.client().patch('/actors/1',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        patch_movie=self.client().patch('/movies/1',headers={'Authorization':"Bearer {}".format(self.casting_director)})

        self.assertEqual(get_actors.status_code,200)
        self.assertEqual(get_movies.status_code,200)
        self.assertNotEqual(post_actor.status_code,401 and 403)
        self.assertEqual(delete_actor.status_code,200)
        self.assertNotEqual(patch_actor.status_code,401 and 403)
        self.assertNotEqual(patch_movie.status_code,401 and 403)
    
    def test_403_casting_director(self):
        ''' tests all the forbidden endpoints for the casting director role'''
        post_movie=self.client().post('/movies',headers={'Authorization':"Bearer {}".format(self.casting_director)})
        delete_movie=self.client().delete('/movies/6',headers={'Authorization':"Bearer {}".format(self.casting_director)})

        self.assertEqual(post_movie.status_code,403)
        self.assertEqual(delete_movie.status_code,403)
    
    # Executive Producer

    def test_executive_producer_allowed_actions(self):
        '''tests allowed endpoints for the executive producer'''
        get_actors=self.client().get('/actors',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        get_movies=self.client().get('/movies',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        post_actor=self.client().post('/actors',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        post_movie=self.client().post('/movies',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        delete_movie=self.client().delete('/movies/8',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        delete_actor=self.client().delete('/actors/8',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        patch_actor=self.client().patch('/actors/1',headers={'Authorization':"Bearer {}".format(self.executive_producer)})
        patch_movie=self.client().patch('/movies/1',headers={'Authorization':"Bearer {}".format(self.executive_producer)})

        self.assertEqual(get_actors.status_code,200)
        self.assertEqual(get_movies.status_code,200)
        self.assertNotEqual(post_actor.status_code,401 and 403)
        self.assertNotEqual(post_movie.status_code,401 and 403)
        self.assertEqual(delete_actor.status_code,200)
        self.assertEqual(delete_movie.status_code,200)
        self.assertNotEqual(patch_actor.status_code,401 and 403)
        self.assertNotEqual(patch_movie.status_code,401 and 403)

    ########### ENPOINTS TESTS ###################
    # Actors tests:

    def test_200_get_actors(self):
        'tests getting all actors in the expected format'
        res=self.client().get('/actors',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        actors=Actors.query.all()
        actors_format_list=[i.format() for i in actors]

        self.assertEqual(200,res.status_code)
        self.assertEqual(len(actors),data['total_actors'])
        self.assertListEqual(actors_format_list[:10], data['actors'])

    
    def test_404_for_invalid_actors_page(self):
        '''tests if the requested actors page is beyond valid index'''
        res=self.client().get('/actors?page=9999',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'resource not found')
    
    def test_success_paginate_actors(self):
        '''tests if the requested actors page works fine'''
        res=self.client().get('/actors?page=1',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        actors=Actors.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_actors'], len(actors))
        self.assertEqual(len(data['actors']), 10)
    
    def test_200_delete_actor(self):
        '''tests if deleting an actor works fine'''
        res=self.client().delete('/actors/4',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        deleted=Actors.query.filter(Actors.id==4).one_or_none()
        actors=Actors.query.all()

        self.assertTrue(data['success'])
        self.assertEqual(deleted,None)
        self.assertEqual(data['deleted'],4)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(actors),data['total_actors'])
    
    def test_404_cant_delete_unexisted_actor(self):
        '''tests if the requested actor does not exist'''
        res=self.client().delete('/actors/9999',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        actor=Actors.query.filter(Actors.id==9999).one_or_none()

        self.assertEqual(res.status_code,404)
        self.assertEqual(actor,None)
        self.assertEqual(data['message'],'resource not found')
        self.assertFalse(data['success'])
    
    
    
    def test_200_add_actor(self):
        '''tests if adding a new actor works fine '''
        
        res=self.client().post('/actors',json=self.new_actor,headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        added_to_db=Actors.query.filter(Actors.name==self.new_actor['name']).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertNotEqual(added_to_db,None)
        self.assertEqual(data['inserted'],added_to_db.name)
        self.assertTrue(data['success'])
    
    def test_422_no_repeated_actors_allowed(self):
        ''' tests an unprocessable unity when adding and already existing actor'''
        res=self.client().post('/actors',json=self.new_actor,headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        actor=Actors.query.filter(Actors.name==self.new_actor['name']).all()

        self.assertEqual(res.status_code,422)
        self.assertNotEqual(0,len(actor))
        self.assertFalse(data['success'])
    
    def test_200_patch_actor(self):
        '''tests if patching and actor works fine'''
        res=self.client().patch('/actors/1',json={'name':'aymen boudabia','age':25},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        modified=Actors.query.filter(Actors.id==1).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'],1)
        self.assertEqual(modified.name,'aymen boudabia')
        self.assertEqual(modified.age,25)
    
    def test_400_patch_actor_with_empty_body(self):
        '''tests a bad request response by patching an actor with an empty body'''
        res=self.client().patch('actors/1',json={},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,400)

    def test_400_patch_actor_with_invalid_age(self):
        '''tests a bad request response by patching an actor's age with invalid data '''
        res=self.client().patch('actors/1',json={'age':5.3},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,400)

    def test_400_patch_actor_with_invalid_gender(self):
        '''tests a bad request response by patching an actor's gender with invalid data '''
        res=self.client().patch('actors/1',json={'gender':'hotmail'},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,400)
    





    #Movies tests

    def test_200_get_movies(self):
        'tests getting all movies in the expected format'
        res=self.client().get('/movies',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        movies=Movies.query.all()

        self.assertEqual(200,res.status_code)
        self.assertEqual(len(movies),data['total_movies'])
        self.assertEqual(list, type(data['movies']))

    def test_404_for_invalid_movies_page(self):
        '''tests if the requested movies page is beyond valid index'''
        res=self.client().get('/movies?page=9999',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'resource not found')
    
    def test_success_paginate_movies(self):
        '''tests if the requested movies page works fine'''
        res=self.client().get('/movies?page=1',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        movies=Movies.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_movies'], len(movies))
        self.assertEqual(len(data['movies']), 10)

    
    def test_200_delete_movie(self):
        '''tests if deleting a movie works fine'''
        res=self.client().delete('/movies/4',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        deleted=Movies.query.filter(Movies.id==4).one_or_none()
        movies=Movies.query.all()

        self.assertTrue(data['success'])
        self.assertEqual(deleted,None)
        self.assertEqual(data['deleted'],4)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(movies),data['total_movies'])
    
    def test_404_cant_delete_unexisted_movie(self):
        '''tests if the requested movie does not exist'''
        res=self.client().delete('/movies/9999',headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        movie=Movies.query.filter(Movies.id==9999).one_or_none()

        self.assertEqual(res.status_code,404)
        self.assertEqual(movie,None)
        self.assertEqual(data['message'],'resource not found')
        self.assertFalse(data['success'])
    
    
    def test_200_add_movie(self):
        '''tests if adding a new movie works fine '''
        
        res=self.client().post('/movies',json=self.new_movie,headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        added_to_db=Movies.query.filter(Movies.title==self.new_movie['title']).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertNotEqual(added_to_db,None)
        self.assertEqual(data['inserted'],added_to_db.title)
        self.assertTrue(data['success'])
    
    def test_422_no_repeated_movies_allowed(self):
        ''' tests an unprocessable unity when adding and already existing movie'''
        res=self.client().post('/movies',json=self.new_movie,headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        movie=Movies.query.filter(Movies.title==self.new_movie['title']).all()

        self.assertEqual(res.status_code,422)
        self.assertNotEqual(0,len(movie))
        self.assertFalse(data['success'])
    
    
    def test_200_patch_movie(self):
        '''tests if patching a movie works fine'''
        res=self.client().patch('/movies/1',json={'release_date':'1994-09-23'},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)
        modified=Movies.query.filter(Movies.id==1).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'],1)
        self.assertEqual(modified.release_date,'1994-09-23')
    
    def test_400_patch_movie_with_empty_body(self):
        '''tests a bad request response by patching a movie with an empty body'''
        res=self.client().patch('movies/1',json={},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,400)

    def test_400_patch_movie_with_invalid_date(self):
        '''tests a bad request response by patching an movie's date with invalid data '''
        res=self.client().patch('movies/1',json={'release_date':'20009-05-66'},headers={"Authorization":"Bearer {}".format(self.executive_producer)})
        data=json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,400)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
