from flask import render_template, Blueprint
from flask.helpers import flash
from flask_login import login_required


# create blueprint
main = Blueprint('main', __name__)


# SECTION routes
@main.route('/')
@login_required
def show_dashboard():
    '''
    Render home page
    '''

    return render_template('dashboard.html')


@main.route("/nutrition/")
@login_required
def show_nutrition_page():
    '''
    GET /nutrition
    ----------------------------------------------------------------
    - Load nutrition page
    '''

    return render_template('nutrition.html')
