import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json
from datetime import datetime
import urllib.parse

from database.models import db_drop_and_create_all, setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  #print("Seting up app")
  app = Flask(__name__)
  #CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.route('/')
  def index():
    return jsonify ({'message': 'Welcome to Casting Agency!'})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  setup_db(app)
  #migrate = Migrate(app, db)


  '''
  @DONE implement endpoint
    GET /actors
      it should require the 'get:actors' permission 
    returns status code 200 and json {"success": True, "actors": actors} where the actors is 
      the list of actors or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=["GET"])
  def actors():
    all_actors = Actor.query.all()

    if len(all_actors) == 0:
      abort(404)

    #print(all_actors)

    actors_list = [i.format() for i in all_actors]

    return jsonify({
      'success': True,
      'actors': len(all_actors),
      'actors_list': actors_list
    })


  '''
  @DONE implement endpoint 
    GET /actors/<int: id>
      it should require the 'get:actors' permission 
    return status code 200 and json {"success": True, "actors": actors} where the actors is 
      the list of actors or appropriate status code indicating reason for failure  
  '''
  @app.route('/actors/<int:actor_id>', methods=["GET"])
  #@requires_auth('get:actors')
  def get_actor_detail(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)

    all_actors = Actor.query.all()

    return jsonify({
      'success': True,
      'actor': actor.format(),
      'id': actor.id,
      'actors': len(all_actors)
    })



  '''
  @DONE implement endpoint
    POST /actors 
      it should require the 'post:actors' permission 
    return status code 200 and json {"success": True, "id": id, "actors": actors} where the actors is 
      the list of actors and id is the id of the new actor or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/actors', methods=["POST"])
  #@requires_auth('post:actors')
  def add_actor():
    try: 
      data = request.get_json()
      name = data.get('name', '')
      gender = data.get('gender', '')
      age = data.get('age', '')
      imagelink = data.get('imagelink', '')
      catchphrase = data.get('catchphrase', None)

      if (name == '' or gender == '' or age == ''):
        abort(422)
      
      actor = Actor(name=name, gender=gender, age=age, imagelink=imagelink, catchphrase=catchphrase)
      actor.insert()
    except:
      abort(422)

    return jsonify({
      'success': True,
      'created': actor.id,
      'actors': len(Actor.query.all())
    })



  '''
  @TODO implement endpoint 
    PATCH /actors/<int: id>
      it should require the 'patch:actors' permission 
    return status code 200 and json {"success": True, "actors": actors} where the actors is 
      the list of actors or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=["PATCH"])
  #@requires_auth('patch:actors')
  def edit_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)

    data = request.get_json()
    print(data)
    name = data.get('name', '')
    gender = data.get('gender', '')
    age = data.get('age', '')
    imagelink = data.get('imagelink', '')
    catchphrase = data.get('catchphrase', None)

    if (name == '' or gender == '' or age == ''):
      abort(422)
    

    actor.name = name
    actor.gender = gender 
    actor.age = age 
    actor.imagelink = urllib.parse.urlencode(imagelink)
    actor.catchphrase = catchphrase 
    print(catchphrase)

    actor.update()

    return jsonify({
      'success': True, 
      'updated': actor.id, 
      'actors': Actor.query.all()
    })


  '''
  @DONE implement endpoint
    DELETE /actors/<int: id>
      it should require the 'delete:actors' permission 
    return status code 200 and json {"success": True, "id": id, "actors": actors} where the actors is 
      the list of actors and id is the id of the deleted actor or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=["DELETE"])
  #@requires_auth('delete:actors')
  def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)

    actor_id = actor.id 
    actor.delete()

    return jsonify({
      'success': True,
      'deleted': actor_id,
      'actors': Actor.query.all()
    })


  '''
  @DONE implement endpoint
    GET /movies 
      it should require the 'get:movies' permission 
    return status code 200 and json {"success": True, "movies": movies} where the actors is 
      the list of movies or appropriate status code indicating reason for failure 
  '''
  @app.route('/movies', methods=["GET"])
  def movies():
    all_movies = Movie.query.all()

    if len(all_movies) == 0:
      abort(404)

    movies_list = [movie.format() for movie in all_movies]

    #for i in movies_list:
    #  print(i)

    return jsonify({
      'success': True,
      'movies_list': movies_list,
      'movies': len(all_movies)
    })

  '''
  @DONE implement endpoint 
    GET /movies/<int: id>
      it should require the 'get:movies' permission 
    return status code 200 and json {"success": True, "movies": movies} where the actors is 
      the list of movies or appropriate status code indicating reason for failure  
  '''
  @app.route('/movies/<int:movie_id>', methods=["GET"])
  #@requires_auth('get:movies')
  def get_movie_detail(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      abort(404)

    return jsonify({
      'success': True,
      'movie': movie.format(),
      'id': movie.id,
      'movies': len(Movie.query.all())
    })



  '''
  @DONE implement endpoint
    POST /movies
      it should require the 'post:movies' permission 
    return status code 200 and json {"success": True, "id": id, "movies": movies} where the actors is 
      the list of movies and id is the id of the new movie or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/movies', methods=["POST"])
  #@requires_auth('post:movies')
  def add_movies():
    data = request.get_json()
    title = data.get('title', '')
    imagelink = data.get('imagelink', '')
    year = data.get('year', '')

    if (title == '' or year == ''):
      abort(422)
    
    year = year + '/01/01'
    year_formatted = datetime.strptime(year, "%Y/%m/%d")
    print(year_formatted)

    movie = Movie(title=title, imagelink=imagelink, year=year_formatted)
    #print(movie.format())
    movie.insert()

    return jsonify({
      'success': True,
      'created': movie.id,
      'movies': len(Movie.query.all())
    }) 

  '''
  @TODO implement endpoint 
    PATCH /movies/<int: id>
      it should require the 'patch:movies' permission 
    return status code 200 and json {"success": True, "movies": movies} where the actors is 
      the list of movies or appropriate status code indicating reason for failure  
  '''
  @app.route('/movies/<int:movie_id>', methods=["PATCH"])
  #@requires_auth('patch:movies')
  def edit_movies(movie_id):
    movie = Actor.query.filter(Actor.id == movie_id).one_or_none()

    if movie is None:
      abort(404)

    data = request.get_json()
    title = data.get('title', '')
    imagelink = data.get('imagelink', '')
    year = data.get('year', '')

    if (title == '' or year == ''):
      abort(422)

    movie.title = title 
    movie.year = year 

    movie.update()

    return jsonify({
      'success': True, 
      'updated': movie.id, 
      'actors': Movie.query.all()
    })


  '''
  @DONE implement endpoint 
    DELETE /movies/<int: id>
      it should require the 'delete:movies' permission 
    return status code 200 and json {"success": True, "id": id, "movies": movies} where the actors is 
      the list of movies and id is the id of the deleted movie or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=["DELETE"])
  #@requires_auth('delete:movies')
  def delete_movies(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      abort(404)

    movie_id = movie.id 
    movie.delete()

    return jsonify({
      'success': True,
      'deleted': movie_id,
      'movies': Movie.query.all()
    })

    
  '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(405)
  def not_allow(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
