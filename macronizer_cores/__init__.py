from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

CURRENT_USER = "user_id"

# create Flask app object
app = Flask(__name__)
app.config.from_object(Config)

# instantiate the extension
debug = DebugToolbarExtension(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from macronizer_cores import routes
from macronizer_cores.errors.routes import errors
from macronizer_cores.auth.routes import auth

# register blueprint to application object
app.register_blueprint(errors)
app.register_blueprint(auth)



