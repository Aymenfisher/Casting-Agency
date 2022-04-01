import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth.auth import AuthError, requires_auth
from datetime import datetime

#Pagination function:
DATA_PER_PAGE = 10
def paginations(request,data):
  page=request.args.get('page',1,type=int)

  start=(page-1)*DATA_PER_PAGE
  end=start+DATA_PER_PAGE
  data_list=[i.format() for i in data]
  page_data=data_list[start:end]
  if len(page_data)==0:
    abort(404)

  return page_data


#Creating the app
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app,resources={r'/*':{'origins':'*'}})
  setup_db(app) #configure the app and initiate the database


  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE')
    return response

  #ENDPOINTS:
  
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors():
    actors=Actors.query.all()
    
    if len(actors)==0:
      abort(404)
    
    return jsonify({
      'actors': paginations(request,actors),
      'total_actors': len(actors)
    })

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies():
    movies=Movies.query.all()
    
    if len(movies)==0:
      abort(404)
    
    return jsonify({
      'movies': paginations(request,movies),
      'total_movies': len(movies)
    })
    
  @app.route('/actors',methods=['POST'])
  @requires_auth('post:actors')
  def create_actor():
    actor=request.get_json()

    if actor==None: #no body
      abort(400)
    elif len(actor)==0:
      abort(400)
    
    if 'name' and 'age' and 'gender' not in actor: #request body must contain all necessary informations.
      abort(400)
    elif type(actor['age']) != int or  actor['gender'].lower() not in ['male','female']: #correct expected format
      abort(400)

    #No repeated actors allowed:
    actor_existance=Actors.query.filter(Actors.name==actor['name']).all() #actors can have same name
    if len(actor_existance) != 0:
      for a in actor_existance:
        if a.age==actor['age']:
          abort(422)

    try:
      new_actor=Actors(name=actor['name'],age=actor['age'],gender=actor['gender'])
      new_actor.insert()
      actors=Actors.query.all()
      return jsonify({
        'success':True,
        'inserted':actor['name'],
        'total_actors': len(actors)
      })
    except:
      abort(422)
    
  @app.route('/movies',methods=['POST'])
  @requires_auth('post:movies')
  def create_movie():
    movie=request.get_json()
    if movie==None:
      abort(400)
    elif len(movie)==0:
      abort(400)
    #checking the correct format of the request body

    if 'title' and 'release_date' not in movie: #request body must contain all necessary informations.
      abort(400)
    
    try: #checking the format and the validity of the release date, must be yyyy-mm-dd
      res = datetime.strptime(movie['release_date'], "%Y-%m-%d")
    except:
      abort(400)
    
    #No repeated movies allowed:
    movie_existance=Movies.query.filter(Movies.title==movie['title']).all() #multiple movies can have same title
    if len(movie_existance) != 0:
      for m in movie_existance:
        if m.release_date==movie['release_date']:
          abort(422)
    #####
    try:
      new_movie=Movies(title=movie['title'],release_date=movie['release_date'])
      new_movie.insert()

      movies=Movies.query.all()

      return jsonify({
        'success':True,
        'inserted':movie['title'],
        'total_actors': len(movies)
        })
    except:
      abort(422)
      
  @app.route('/actors/<int:actor_id>',methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(actor_id):
    #checking if the actor exists:
    actor=Actors.query.filter(Actors.id==actor_id).one_or_none()
    if actor is None:
      abort(404)
    #deleting
    try:
      actor.delete()

      actors=Actors.query.all()

      return jsonify({
        'success':True,
        'deleted':actor_id,
        'total_actors':len(actors)
      })
    except:
      abort(422)

      
  @app.route('/movies/<int:movie_id>',methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(movie_id):
    #checking if the movie exists:
    movie=Movies.query.filter(Movies.id==movie_id).one_or_none()
    if movie is None:
      abort(404)
    #deleting
    try:
      movie.delete()

      movies=Movies.query.all()

      return jsonify({
        'success':True,
        'deleted':movie_id,
        'total_movies':len(movies),
      })
    except:
      abort(422)
        
  @app.route('/actors/<int:actor_id>',methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(actor_id):
    #Checking if the actor exists
    actor=Actors.query.filter(Actors.id==actor_id).one_or_none()
    if actor is None:
      abort(404)
    #Patching:
    new_actor=request.get_json()

    if new_actor==None :
      abort(400)
    elif len(new_actor)==0:
      abort(400)
    
    for attribute in new_actor:
      if attribute=='name':
        actor.name=new_actor['name']
      elif attribute=='age':
        if type(new_actor['age'])!= int :
          abort(400)
        actor.age=new_actor['age']
      elif attribute=='gender':
        if new_actor['gender'].lower() not in ['male','female']:
          abort(400)
        actor.gender=new_actor['gender']
      else:
        abort(400)
    try:
      actor.update()
      actors=Actors.query.all()
      return jsonify({
        'success':True,
        'updated':actor.id,
        'total_actors':len(actors)
        })
    except:
      abort(422)
      
  @app.route('/movies/<int:movie_id>',methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(movie_id):
    #Checking if the movie exists
    movie=Movies.query.filter(Movies.id==movie_id).one_or_none()
    if movie is None:
      abort(404)
    #Patching:
    new_movie=request.get_json()
    if new_movie==None: #empty body
      abort(400)
    elif len(new_movie)==0:
      abort(400)
    
    for attribute in new_movie:
      if attribute=='title':
        movie.name=new_movie['title']
      elif attribute=='release_date':
        try: #checking the format and the validity of the release date, must be yyyy-mm-dd
          res = datetime.strptime(new_movie['release_date'], "%Y-%m-%d")
        except:
          abort(400)
        movie.release_date=new_movie['release_date']
      else:
        abort(400)
    try:
      movie.update()
      movies=Movies.query.all()
      return jsonify({
        'success':True,
        'updated':movie.id,
        'total_movies':len(movies)
      })
    except:
      abort(422)
  
  #### Errors Handlers #####
  @app.errorhandler(404)
  def not_found_404(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'resource not found'
    }),404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':'unprocessable'
    }),422
  
  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':400,
      'message':'Bad request'
    }),400
  

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=bool(os.environ['DEBUG']))