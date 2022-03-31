from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db=SQLAlchemy()

def setup_db(app):
    ''' configure the app and setup the database'''
    app.config.from_pyfile('config.py')
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate=Migrate(app,db)

########## Models ##############

class Movies(db.Model):
    __tablename__="Movies"
    
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(),nullable=False)
    release_date=db.Column(db.String())

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
    
    def format(self):
        return {
            'title':self.title,
            'release_date':self.release_date
        }

class Actors(db.Model):
    __tablename__='Actors'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    age=db.Column(db.Integer)
    gender=db.Column(db.String())

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
    
    def format(self):
        return {
            'name':self.name,
            'age':self.age,
            'gender':self.gender
        }
