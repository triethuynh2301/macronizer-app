from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import DevelopmentConfig


# instantiate the extension
debug = DebugToolbarExtension()
db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()


def create_app(config_class=DevelopmentConfig):
  # create Flask app object
  app = Flask(__name__)
  app.config.from_object(config_class)

  register_extension(app)
  register_blueprint(app)

  return app


def register_blueprint(app):
    '''Helper function to import and register blueprint'''

    # import blueprints
    from macronizer_cores.errors.routes import errors
    from macronizer_cores.auth.routes import auth
    from macronizer_cores.log_api.routes import log_api
    from macronizer_cores.food_item_api.routes import food_item_api
    from macronizer_cores.user_api.routes import user_api
    from macronizer_cores.main.routes import main

  # register blueprints to application object
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(log_api)
    app.register_blueprint(food_item_api)
    app.register_blueprint(user_api)


def register_extension(app):
  '''Helper function to register extension'''

  debug.init_app(app)
  db.init_app(app)
  bcrypt.init_app(app)
  # register flask_login
  login.init_app(app)
  login.login_view = 'auth.login'
  login.login_message_category = 'warning'

