from flask import request, flash, redirect, g, jsonify, Blueprint
from secret_keys import CALORIE_NINJA_API_KEY
from macronizer_cores import db
from macronizer_cores.models import FoodItem
import requests


# create blueprint
food_item_api = Blueprint('food_item_api', __name__)


# SECTION - routes
@food_item_api.route("/api/food/search")
def search_food_item():
    '''
    GET /api/food/search/<string:query_string>
    ----------------------------------------------------------------
    - Search for food in CaloriesNinja using query string from client
    
    Returns
    --------------
    List of food items in JSON format
    '''

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query_string = request.args.get('queryString')
    response = requests.get(api_url + query_string, headers={'X-Api-Key': CALORIE_NINJA_API_KEY})

    if response.status_code == requests.codes.ok:
        # json() returns a JSON object of the result -> return payload data to JSON
        return response.json()
    else:
        # TODO - add error handling
        print("Error:", response.status_code, response.text)


@food_item_api.route("/api/food/delete/<int:food_id>", methods=["DELETE"])
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

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

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
