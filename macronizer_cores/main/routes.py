from flask import render_template, Blueprint
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

    return render_template('content/dashboard.html')


@main.route("/nutrition")
@login_required
def show_nutrition_page():
    '''
    GET /nutrition
    ----------------------------------------------------------------
    - Load nutrition page
    '''

    return render_template('content/nutrition.html')

@main.route('/profile')
@login_required
def show_user_profile():
    '''
    GET /profile
    ----------------------------------------------------------------
    - Load user profile page
    '''

    return render_template('content/profile.html')
