from flask import Blueprint, render_template
from macronizer_cores import db


# create error blueprint
errors = Blueprint('errors', __name__)


# SECTION - routes
# NOTE - app_errorhandler() is a method inherited from Blueprint that is equivalent to errorhandler() inherited from flask
@errors.app_errorhandler(404)
def page_not_found(e):
    '''Handle 404 error'''

    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
  '''Handle 500 error'''

  db.session.rollback()
  return render_template('errors/500.html'), 500