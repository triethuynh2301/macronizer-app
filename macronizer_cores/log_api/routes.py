from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from macronizer_cores import db
from macronizer_cores.models import Log, FoodItem
from macronizer_cores.log_api.utils import create_food_log 
from datetime import datetime


# create blueprint
log_api = Blueprint('log_api', __name__)


# SECTION - routes
@log_api.route("/api/log/search")
@login_required
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
                    Log.user_id == current_user.id)\
                .all()

    # serialize data
    meals = [meal.serialize() for meal in meals]

    # return list of meals log in JSON
    return jsonify(meals_logged=meals)


@log_api.route("/api/log/new", methods=["POST"])
@login_required
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
    new_log = create_food_log(current_user.id, date_string, meal_no, food_list)
    
    try:
        db.session.add(new_log)
        db.session.commit()

        # jsonify() turn dict into json format
        res = jsonify(log=new_log.serialize())
        return (res, 201)
    except:
        res = {"message": "Server Error"}
        return (res, 500)


@log_api.route("/api/log/update", methods=["PATCH"])
@login_required
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
            user_id=current_user.id)\
        .first()
    
    # get the food item 
    updated_item = FoodItem.query.get_or_404(updated_item_id)

    try:
        # create the log if not existed
        if updated_log is None:
            updated_log = Log(
                meal_no=meal_no,
                date=logged_date,
                user_id=current_user.id,
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

