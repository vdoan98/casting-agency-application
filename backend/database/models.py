import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import datetime

#database_path = os.environ['DATABASE_URL']
database_name = "castingagency"
#postgresql://postgres:DataPass98@localhost:5432/fyyur'
database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'DataPass98','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Person
Have title and release year
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  gender = Column(String)
  age = Column(Integer)
  imagelink = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, gender, age, imagelink, catchphrase=""):
    self.name = name
    self.gender = gender
    self.age = age
    self.imagelink = imagelink
    self.catchphrase = catchphrase

  '''
  insert()
    inserts a new model into a database 
    the model must have a unique id 
    EXAMPLE
      actor = Actor(name=req_name, gender=req_gender, age=req_age, catchphrase=req_phrase)
      actor.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  delete()
    deletes a model in a database 
    the model must exist in the database
    EXAMPLE
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      actor.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  update()
    updates a model in a database
    the model must exist in the database 
    EXAMPLE
      actor = Actor.query.filter(Actor.id == id).one_or_none()
      actor = 'Elizabeth Taylor'
      actor.update()
  '''
  def update(self):
        db.session.commit()
  
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender,
      'age': self.age,
      'imagelink': self.imagelink,
      'catchphrase': self.catchphrase}

'''
Casting Assistant 
'''


'''
Movie
'''
class Movie(db.Model):
  ___tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  imagelink = Column(String)
  year = Column(DateTime)


  def __init__(self, title, year, imagelink):
    self.title = title
    self.imagelink = imagelink
    self.year = year 


  '''
  insert()
    inserts a new model into a database 
    the model must have a unique id 
    EXAMPLE
      movie = Movie(title=req_title, year=req_year)
      movie.insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()

  '''
  delete()
    deletes a model in a database 
    the model must exist in the database
    EXAMPLE
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      movie.delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  '''
  update()
    updates a model in a database
    the model must exist in the database 
    EXAMPLE
      movie = Movie.query.filter(Movie.id == id).one_or_none()
      movie = 'Gentlemen Prefer Blondes'
      movie.update()
  '''
  def update(self):
        db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'year': self.year.strftime('%Y'),
      'imagelink': self.imagelink
    }