from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

CURRENT_USER = "user_id"

# instantiate the extension
debug = DebugToolbarExtension()
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
  # create Flask app object
  app = Flask(__name__)
  app.config.from_object(Config)

  # register extension
  debug.init_app(app)
  db.init_app(app)
  bcrypt.init_app(app)

  # import blueprints
  from macronizer_cores.errors.routes import errors
  from macronizer_cores.auth.routes import auth
  from macronizer_cores.log_api.routes import log_api
  from macronizer_cores.food_item_api.routes import food_item_api
  from macronizer_cores.main.routes import main

  # register blueprints to application object
  app.register_blueprint(main)
  app.register_blueprint(errors)
  app.register_blueprint(auth)
  app.register_blueprint(log_api)
  app.register_blueprint(food_item_api)

  return app



