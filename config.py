import os


#Debug mode.
DEBUG = os.environ['DEBUG']

#Track modifications
SQLALCHEMY_TRACK_MODIFICATIONS=False

#DATABASE URL
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URI = database_path