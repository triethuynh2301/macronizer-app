from datetime import datetime
from app.models import Log, FoodItem

def create_food_log(user_id, date_string, meal_no, item_list) -> Log:
    '''
    Helper method to construct a food log object from date string, meal number, and
    food items list
    '''

    # convert query parameter to date
    logged_date = datetime.strptime(date_string, '%Y-%m-%d').date()

    # convert food item json into FoodItem object
    food_list = []
    for item in item_list:
        new_item = FoodItem(
            name=item.get("name"),
            sugar_gram = item.get("sugar"),
            fiber_gram = item.get("fiber"),
            serving_size_gram = item.get("servingSize"),
            sodium_mg = item.get("sodium"),
            potassium_mg = item.get("potassium"),
            fat_saturation_gram = item.get("saturatedFat"),
            fat_total_gram = item.get("totalFat"),
            calories = item.get("calories"),
            cholesterol_mg = item.get("cholesterol"),
            protein_gram = item.get("protein"),
            carbohydrate_gram = item.get("carbohydrate")
        )
        food_list.append(new_item)
    
    # return new Log object
    return Log(
        meal_no=meal_no,
        date=logged_date,
        user_id=user_id,
        food_items=food_list
    )