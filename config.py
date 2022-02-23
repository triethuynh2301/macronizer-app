from distutils.debug import DEBUG
import os
from dotenv import load_dotenv


# load the .env
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# API key and env variables
CALORIES_NINJA_API_KEY = os.getenv('CALORIES_NINJA_API_KEY')
FLASK_ENV = os.getenv('FLASK_ENV')


# SECTION - config classes
class Config(object):
  '''
  Config parent class
  '''

  SECRET_KEY = os.getenv('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
  '''
  Config for production
  '''

  DEBUG = False
  # db config
  uri = os.getenv("DATABASE_URL") 
  if uri and uri.startswith("postgres://"):
      uri = uri.replace("postgres://", "postgresql://", 1)
  SQL_DATABASE_URI = uri

  


class DevelopmentConfig(Config):
  '''
  Config for developement (inherited from super class Config)
  '''

  DEBUG = True
  # Flask debugtoolbar config
  DEBUG_TB_INTERCEPT_REDIRECTS = False
  # db config
  SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DB_URL")


class TestConfig(Config):
  '''
  Config to run unit and integration test
  '''

  # Enable testing mode. Exceptions are propagated rather than handled by the the app’s error handlers
  DEBUG = False
  TESTING = True
  # disable @login_required 
  LOGIN_DISABLED = True
  SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL')
  WTF_CSRF_ENABLED = False
