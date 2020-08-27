import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json
from datetime import datetime
import urllib.parse

from database.models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  #print("Seting up app")
  app = Flask(__name__)
  #CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  #db_drop_and_create_all()

  @app.route('/')
  def index():
    return jsonify ({'message': 'Welcome to Casting Agency!'})

  @app.after_request
  def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response


  setup_db(app)
  #migrate = Migrate(app, db)
  movie1 = Movie(title='How to Steal a Million', year=datetime.strptime('1966/01/01', "%Y/%m/%d"))
  movie2 = Movie(title='How to Marry a Millionaire', year=datetime.strptime('1953/01/01', "%Y/%m/%d"))
  movie3 = Movie(title='Sunset Boulevard', year=datetime.strptime('1950/01/01', "%Y/%m/%d"))
  movie4 = Movie(title='The Misfits' , year=datetime.strptime('1961/01/01', "%Y/%m/%d"))
  movie5 = Movie(title='All About Eve', year=datetime.strptime('1950/01/01', "%Y/%m/%d"))
  movie6 = Movie(title='Gentlemen Prefer Blondes', year=datetime.strptime('1953/01/01', "%Y/%m/%d"))
  movie7 = Movie(title='The Seven Year Itch', year=datetime.strptime('1955/01/01', "%Y/%m/%d"))
  movie8 = Movie(title='Pillow Talk', year=datetime.strptime('1959/01/01', "%Y/%m/%d"))
  movie9 = Movie(title='High Society', year=datetime.strptime('1956/01/01', "%Y/%m/%d"))
  movie10 = Movie(title='The King and I', year=datetime.strptime('1956/01/01', "%Y/%m/%d"))


  movie1.insert()
  movie2.insert()
  movie3.insert()
  movie4.insert()
  movie5.insert()
  movie6.insert()
  movie7.insert()
  movie8.insert()
  movie9.insert()
  movie10.insert()

  artist1 = Actor(name='Marilyn Monroe', gender='female', age=23, catchphrase='Keep smiling, because life is a beautiful thing and theres so much to smile about.')
  artist2 = Actor(name='Joan Crawford', gender='female', age=28, catchphrase='')
  artist3 = Actor(name='Elizabet Taylor', gender='female', age=25, catchphrase='')
  artist4 = Actor(name='Paul Newman', gender='male', age=35, catchphrase='If you dont have enemies, you dont have character.')
  artist5 = Actor(name='Grace Kelly', gender='female', age=27, catchphrase='')
  artist6 = Actor(name='Tommy Noonan', gender='male', age=28, catchphrase='') 
  artist7 = Actor(name='Elliot Reid', gender='male', age=30, catchphrase='')
  artist8 = Actor(name='Jane Russell', gender='female', age=27, catchphrase='')
  artist9 = Actor(name='Charles Coburn', gender='male', age=67, catchphrase='')
  artist10 = Actor(name='Gloria Swanson', gender='female', age=32, catchphrase='') 

  artist1.insert()
  artist2.insert()
  artist3.insert()
  artist4.insert()
  artist5.insert()
  artist6.insert()
  artist7.insert()
  artist8.insert()
  artist9.insert()
  artist10.insert()


  '''
  @DONE implement endpoint
    GET /actors
      it should require the 'get:actors' permission 
    returns status code 200 and json {"success": True, "actors": actors} where the actors is 
      the list of actors or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=["GET"])
  @requires_auth('get:actors')
  def actors(jwt):
    all_actors = Actor.query.all()

    if len(all_actors) == 0:
      abort(404)
  
    #comment

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
  @requires_auth('get:actors')
  def get_actor_detail(jwt, actor_id):
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
  @requires_auth('post:actors')
  def add_actor(jwt):
    try: 
      data = request.get_json()
      name = data.get('name', '')
      gender = data.get('gender', '')
      age = data.get('age', '')
      catchphrase = data.get('catchphrase', None)

      if (name == '' or gender == '' or age == ''):
        abort(422)
      
      actor = Actor(name=name, gender=gender, age=age, catchphrase=catchphrase)
      actor.insert()
    except:
      abort(422)

    return jsonify({
      'success': True,
      'created': actor.id,
      'actors': len(Actor.query.all())
    })



  '''
  @DONE implement endpoint 
    PATCH /actors/<int: id>
      it should require the 'patch:actors' permission 
    return status code 200 and json {"success": True, "actors": actors} where the actors is 
      the list of actors or appropriate status code indicating reason for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=["PATCH"])
  @requires_auth('patch:actors')
  def edit_actor(jwt, actor_id):
    try: 
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      print(actor.format())

      if actor is None:
        abort(404)

      data = request.get_json()
      name = data.get('name', '')
      gender = data.get('gender', '')
      age = data.get('age', '')
      catchphrase = data.get('catchphrase', None)

      if (name == '' or gender == '' or age == ''):
        abort(422)
      

      actor.name = name
      actor.gender = gender 
      actor.age = age 
      actor.catchphrase = catchphrase 
      actor.update()
      print(actor.format())

      return jsonify({
        'success': True, 
        'updated': actor.id, 
        'actors': len(Actor.query.all())
      })
    except Exception as e:
      print(e)
      abort(422)


  '''
  @DONE implement endpoint
    DELETE /actors/<int: id>
      it should require the 'delete:actors' permission 
    return status code 200 and json {"success": True, "id": id, "actors": actors} where the actors is 
      the list of actors and id is the id of the deleted actor or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/actors/<int:actor_id>', methods=["DELETE"])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
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
  @requires_auth('get:movies')
  def movies(jwt):
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
  @requires_auth('get:movies')
  def get_movie_detail(jwt, movie_id):
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
  @requires_auth('post:movies')
  def add_movies(jwt):
    try: 
      data = request.get_json()
      title = data.get('title', '')
      year = data.get('year', '')

      if (title == '' or year == ''):
        abort(422)
      
      year = year + '/01/01'
      year_formatted = datetime.strptime(year, "%Y/%m/%d")
      #print(year_formatted)

      movie = Movie(title=title, year=year_formatted)
      #print(movie.format())
      movie.insert()

      return jsonify({
        'success': True,
        'created': movie.id,
        'movies': len(Movie.query.all())
      })
    except:
      abort(422)


  '''
  @TODO implement endpoint 
    PATCH /movies/<int: id>
      it should require the 'patch:movies' permission 
    return status code 200 and json {"success": True, "movies": movies} where the actors is 
      the list of movies or appropriate status code indicating reason for failure  
  '''
  @app.route('/movies/<int:movie_id>', methods=["PATCH"])
  @requires_auth('patch:movies')
  def edit_movies(jwt, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      print(movie.format())
      if movie == None:
        abort(404)

      data = request.get_json()
      title = data.get('title', '')
      year = data.get('year', '')

      if (title == '' or year == ''):
        abort(422)

      year = year + '/01/01'
      year_formatted = datetime.strptime(year, "%Y/%m/%d")

      movie.title = title 
      movie.year = year_formatted 

      movie.update()
      print(movie.format())

      return jsonify({
        'success': True, 
        'updated': movie.id, 
        'movies': len(Movie.query.all())
      })
    except:
      abort(422)


  '''
  @DONE implement endpoint 
    DELETE /movies/<int: id>
      it should require the 'delete:movies' permission 
    return status code 200 and json {"success": True, "id": id, "movies": movies} where the actors is 
      the list of movies and id is the id of the deleted movie or appropriate status code indicating reason 
      for failure
  '''
  @app.route('/movies/<int:movie_id>', methods=["DELETE"])
  @requires_auth('delete:movies')
  def delete_movies(jwt, movie_id):
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

  @app.errorhandler(AuthError)
  def auth_error(error):
    error_details = error.error
    error_status_code = error.status_code 

    return jsonify({
      "success": False,
      "error": error_status_code,
      "message": error_details['description']
    }), error_status_code

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
