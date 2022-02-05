from flask import redirect, render_template, g, jsonify, Blueprint
from flask.helpers import flash
from macronizer_cores.log_api.utils import create_food_log


# create blueprint
main = Blueprint('main', __name__)


# SECTION routes
@main.route('/')
def show_dashboard():
    '''
    Render home page
    '''

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")


    return render_template('dashboard.html')


# ----------------------------------------------------------------
# SECTION Nutrtion routes
# ----------------------------------------------------------------
@main.route("/nutrition/")
def show_nutrition_page():
    '''
    GET /nutrition
    ----------------------------------------------------------------
    - Load nutrition page
    '''

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    return render_template('nutrition.html')
