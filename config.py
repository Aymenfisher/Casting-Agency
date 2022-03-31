import os


#Debug mode.
DEBUG = os.environ['DEBUG']

#Track modifications
SQLALCHEMY_TRACK_MODIFICATIONS=False

#DATABASE URL
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']