from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

# create Flask app object
app = Flask(__name__)

# Flask debugtoolbar config
app.config.from_object(Config)
debug = DebugToolbarExtension(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

CURRENT_USER = "user_id"

from app import routes, models, forms, utils
