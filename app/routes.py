from flask import request, redirect, render_template, session, g, jsonify
from flask.helpers import flash
from secret_keys import CALORIE_NINJA_API_KEY
from app import app, db, CURRENT_USER
from app.models import User, Log, FoodItem
from app.utils import create_food_log
from app.forms import LoginForm, RegisterForm
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import requests

# SECTION routes

# ----------------------------------------------------------------
# SECTION error handlers
# ----------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    '''Handle 404 error'''

    return render_template('404.html'), 404


# ----------------------------------------------------------------
# SECTION Authentication routes
# ----------------------------------------------------------------


@app.before_request
def add_user_to_g():
    '''
    If logged in, manage current user session in g variable
    '''

    if CURRENT_USER in session:
        g.user = User.query.get(session.get(CURRENT_USER))
    else:
        g.user = None
    g.today = datetime.now().date()


# ----------------------------------------------------------------
# Turn off all caching in Flask
# @credit to https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
# ----------------------------------------------------------------
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


@app.route('/')
def show_dashboard():
    '''
    Render home page
    '''

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")


    return render_template('dashboard.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    User login
    '''

    remove_user_from_session()
    form = LoginForm()

    # if POST request -> validate data
    if form.validate_on_submit():
        # retrieve form data
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        # check if authentication succeeds
        if user:
            # store user id in session 
            session[CURRENT_USER] = user.id
            return redirect("/")
        else:
            form.username.errors = ["Invalid username/password."]

    # if GET request or authentication fails-> render login form 
    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    '''
    Register user
    '''

    remove_user_from_session()
    form = RegisterForm()

    # if POST request -> validate data
    if form.validate_on_submit():
        # retrieve form data
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # password hashing
        (username, password) = User.register(username, password)

        # add user to db
        try:
            new_user = User(
                name=name, 
                email=email, 
                username=username,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("Username taken.", "warning")
            return redirect("/register")

        # store current user id in session for authentication/authorization
        # and redirect to home page
        session[CURRENT_USER] = new_user.id
        return redirect("/")

    # if GET request, render register form
    return render_template('register.html', form=form)


def remove_user_from_session():
    '''
    if currently logged in -> log out
    '''

    if CURRENT_USER in session:
        # remove key from session
        del session[CURRENT_USER]


# best practice to logout with POST request to prevent caching
@app.route("/logout", methods=["POST"])
def logout():
    '''
    Log user out and redirect back to login page
    '''

    remove_user_from_session()
    flash("You have logged out.", "info")

    return redirect("/login")


# ----------------------------------------------------------------
# SECTION Nutrtion routes
# ----------------------------------------------------------------
@app.route("/nutrition/")
def show_nutrition_page():
    '''
    GET /nutrition
    ----------------------------------------------------------------
    - Load nutrition page
    '''

    return render_template('nutrition.html')


# ----------------------------------------------------------------
# SECTION api/food routes
# ----------------------------------------------------------------
@app.route("/api/food/search")
def search_food_item():
    '''
    GET /api/food/search/<string:query_string>
    ----------------------------------------------------------------
    - Search for food in CaloriesNinja using query string from client
    
    Returns
    --------------
    List of food items in JSON format
    '''

    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query_string = request.args.get('queryString')
    response = requests.get(api_url + query_string, headers={'X-Api-Key': CALORIE_NINJA_API_KEY})

    if response.status_code == requests.codes.ok:
        # json() returns a JSON object of the result -> return payload data to JSON
        return response.json()
    else:
        # TODO - add error handling
        print("Error:", response.status_code, response.text)


@app.route("/api/food/delete/<int:food_id>", methods=["DELETE"])
def delete_food_item_from_log(food_id):
    '''
    DELETE /api/food/delete/<int:food_id>
    ----------------------------------------------------------------
    - Delete a food item from db using item id

    Parameters
    --------------
    food_id: int
        Id of the item to be deleted

    Returns
    --------------
    Food item deleted in JSON format and status code 204 
    '''

    item_to_delete = FoodItem.query.get_or_404(food_id)
    print(f"******{item_to_delete}********")

    try:
        db.session.delete(item_to_delete)
        db.session.commit()

        # jsonify() turn dict into json format
        res = jsonify(log=item_to_delete.serialize())
        return (res, 204)
    except:
        res = {"message": "Server Error"}
        return (res, 500)

# ----------------------------------------------------------------
# SECTION api/log routes
# ----------------------------------------------------------------
@app.route("/api/log/search")
def search_meals_logged_by_date():
    '''
    GET /api/log/search
    ----------------------------------------------------------------
    - Get all meals for current logged-in user by date
    
    Returns
    --------------
    List of meals in JSON format
    '''

    # convert query string to date
    date_string = request.args.get('date')
    search_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    # search for meals logged
    meals = Log.query\
                .filter(
                    Log.date == search_date,
                    Log.user_id == g.user.id)\
                .all()

    # serialize data
    meals = [meal.serialize() for meal in meals]

    # return list of meals log in JSON
    return jsonify(meals_logged=meals)


@app.route("/api/log/new", methods=["POST"])
def log_a_meal():
    '''
    POST /api/log/new
    ----------------------------------------------------------------
    - Log a meal for a particular date and meal no

    Returns
    --------------
    List of food items logged for a particular date and meal in JSON format
    '''
    
    # construct a food log object
    food_list = request.json.get("food_items")
    meal_no = request.json.get("meal_no")
    date_string = request.json.get("date_string")
    new_log = create_food_log(g.user.id, date_string, meal_no, food_list)
    
    try:
        db.session.add(new_log)
        db.session.commit()

        # jsonify() turn dict into json format
        res = jsonify(log=new_log.serialize())
        print(res.json)
        return (res, 201)
    except:
        res = {"message": "Server Error"}
        return (res, 500)


@app.route("/api/log/update", methods=["PATCH"])
def update_meal_log():
    '''
    PATCH /api/log/update
    ----------------------------------------------------------------
    - Update a SINLGE food item logged for a particular date and meal no

    Returns
    --------------
    List of food items logged for a particular date and meal in JSON format
    '''

    # convert query parameter to date
    date_string = request.json.get("date_string")
    updated_item_id = request.json.get('updated_item_id')
    meal_no = request.json.get('meal_no')
    logged_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    # get the log
    updated_log = Log\
        .query\
        .filter_by(
            meal_no=meal_no,
            date=logged_date,
            user_id=g.user.id)\
        .first()
    
    # get the food item 
    updated_item = FoodItem.query.get_or_404(updated_item_id)

    try:
        # create the log if not existed
        if updated_log is None:
            updated_log = Log(
                meal_no=meal_no,
                date=logged_date,
                user_id=g.user.id,
                food_items=[updated_item]
            )
            db.session.add(updated_log)

        # reassign food item to correct log
        updated_item.log_id = updated_log.id
        db.session.commit()

        # jsonify() turn dict into json format
        res = jsonify(log=updated_log.serialize())
        return (res, 201)
    except:
        res = {"message": "Server Error"}
        return (res, 500)

