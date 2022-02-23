// const API_LOG_URL = "http://localhost:5000/api/log";
// const API_FOOD_ITEM_URL = "http://localhost:5000/api/food";
// const API_USER_URL = "http://localhost:5000/api/user";
// NOTE - used in production
const API_LOG_URL = "https://macronizer-app.herokuapp.com/api/log";
const API_FOOD_ITEM_URL = "https://macronizer-app.herokuapp.com/api/food";
const API_USER_URL = "https://macronizer-app.herokuapp.com/api/user";

/**************
 * USER MODEL *
 **************/
class User {
  constructor(name, username, email, password) {
    this.name = name;
    this.username = username;
    this.email;
    this.password = password;
  }

  async handleProfileChanges(e) {
    e.preventDefault();

    // extract page data
    const name = document.getElementById("fullName").value;
    const username = document.getElementById("userName").value;
    const email = document.getElementById("email").value;

    // api call
    User.editProfile(name, username, email)
      .then(() => {
        // update UI
        window.location.reload();
      })
      .catch((err) => {
        console.log(err);
      });
  }

  /*************************
   * @PARAM {STRING} NAME  *
   * @PARAM {STRING} EMAIL *
   *************************/
  static async editProfile(name, username, email) {
    try {
      const endpoint = `${API_USER_URL}/edit`;
      const payload = {
        name: name,
        email: email,
        username: username,
      };
      const res = await axios.put(endpoint, payload);
      const { user } = res.data;

      return new User(user.name, user.username, user.email);
    } catch (e) {
      console.error(e);
    }
  }
}

/**
 * Meals logged model
 * @class
 */
class Log {
  /***************************
   *  - Construct Log object *
   * @constructor            *
   ***************************/
  constructor(id, mealNo, date, userId, foodItems) {
    this.id = id;
    this.mealNo = mealNo;
    this.date = date;
    this.userId = userId;
    this.foodItems = foodItems;
  }

  /*********************************************************
   * - GET request to search log by date                *
   * @param {String} - a date in string YYYY-MM-DD format     *
   * @return {Log[]} - list of Log obj for the chosen date *
   *********************************************************/
  static async searchLogByDate(dateString) {
    try {
      const endpoint = `${API_LOG_URL}/search`;
      const res = await axios.get(endpoint, { params: { date: dateString } });

      // convert list of json data list of object
      const mealsLoggedList = res.data.meals_logged.map(
        (log) =>
          new Log(log.id, log.meal_no, log.date, log.user_id, log.food_items)
      );
      return mealsLoggedList;
    } catch (e) {
      console.debug(e);
    }
  }

  /************************************************************************
   * - POST request to log a meal                                         *
   * @param {Number} mealNo                                               *
   * @param {String} date - a date in string format YYYY-MM-DD            *
   * @param {FoodItem[]} foodItems - list of food items to log for the meal *
   ************************************************************************/
  static async logMeal(mealNo, dateString, foodItems) {
    try {
      const endpoint = `${API_LOG_URL}/new`;
      const payload = {
        meal_no: mealNo,
        food_items: foodItems,
        date_string: dateString,
      };

      const res = await axios.post(endpoint, payload);
      const { log } = res.data;
      return new Log(
        log.id,
        log.meal_no,
        log.date,
        log.user_id,
        log.food_items
      );
    } catch (e) {
      console.debug(e);
    }
  }

  /*********************************************************************************
   * - PATCH request to update a meal                                              *
   * @param {Number} mealNo - an integer number                                    *
   * @param {String} date - a date in string format YYYY-MM-DD                     *
   * @param {Number} updatedItemId - an integer no inidicating id of the food item *
   *********************************************************************************/
  static async updateLoggedMeal(mealNo, dateString, updatedItemId) {
    try {
      const endpoint = `${API_LOG_URL}/update`;
      const payload = {
        meal_no: mealNo,
        updated_item_id: updatedItemId,
        date_string: dateString,
      };

      const res = await axios.patch(endpoint, payload);
      const { log } = res.data;
      return new Log(
        log.id,
        log.meal_no,
        log.date,
        log.user_id,
        log.food_items
      );
    } catch (e) {
      console.debug(e);
    }
  }
}

/********************
 * Food Item models
 * @class *
 ********************/
class FoodItem {
  /******************************************************************************
   * - Construct food item object with data retrieved from CaloriesNinja API *
   * @constructor                                                               *
   ******************************************************************************/
  constructor(
    name,
    sugar,
    fiber,
    servingSize,
    sodium,
    potassium,
    saturatedFat,
    totalFat,
    calories,
    cholesterol,
    protein,
    carbohydrate
  ) {
    this.name = name;
    this.sugar = sugar;
    this.fiber = fiber;
    this.servingSize = servingSize;
    this.sodium = sodium;
    this.potassium = potassium;
    this.saturatedFat = saturatedFat;
    this.totalFat = totalFat;
    this.calories = calories;
    this.cholesterol = cholesterol;
    this.protein = protein;
    this.carbohydrate = carbohydrate;
  }

  /*********************************************************
   * - GET request to CaloriesNinja API get food item info *
   * @param {String} - search string input by user
   * @return {FoodItem[]} - list of FoodItem objects       *
   *********************************************************/
  static async searchFoodItem(queryString) {
    try {
      const endpoint = `${API_FOOD_ITEM_URL}/search`;
      const res = await axios.get(endpoint, {
        params: { queryString: queryString },
      });

      // convert list of json data list of object
      const foodItems = res.data.items.map(
        (item) =>
          new FoodItem(
            item.name,
            item.sugar_g,
            item.fiber_g,
            item.serving_size_g,
            item.sodium_mg,
            item.potassium_mg,
            item.fat_saturated_g,
            item.fat_total_g,
            item.calories,
            item.cholesterol_mg,
            item.protein_g,
            item.carbohydrates_total_g
          )
      );
      return foodItems;
    } catch (e) {
      console.debug(e);
    }
  }

  /************************************************************
   * - DELETE request to delete a food item                   *
   * @param {Number} - itemId - id of the food item to delete *
   * @return {Promise} - response from HTTP request           *
   ************************************************************/
  static async deleteFoodItem(itemId) {
    try {
      const endpoint = `${API_FOOD_ITEM_URL}/delete/${itemId}`;
      const res = await axios.delete(endpoint);

      return res;
    } catch (e) {
      console.debug(e);
    }
  }
}
