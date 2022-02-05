from secret_keys import FLASK_SECRET_KEY

class Config(object):
  SECRET_KEY = FLASK_SECRET_KEY

  # Flask debugtoolbar config
  DEBUG_TB_INTERCEPT_REDIRECTS = False

  # Flask SQLAchelmy config
  SQLALCHEMY_DATABASE_URI = 'postgresql:///macronizer_db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False
