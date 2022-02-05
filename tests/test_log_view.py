from unittest import TestCase
from app.routes import app, CURRENT_USER
from app.models import db, User, Log, FoodItem
from datetime import datetime

# set up test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///macronizer_test_db'
app.config['SQLALCHEMY_ECHO'] = False
# Enable testing mode. Exceptions are propagated rather than handled by the the app’s error handlers
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
      """Make demo data."""

      TestCase.maxDiff = None

      u1 = User(
          name="John Doe",
          email="john.doe@gmail.com",
          username="johndoelearntocode",
          password="123456789"
      )
      (u1.username, u1.password) = User.register(u1.username, u1.password)
      self.u1 = u1
      db.session.add(u1)
      db.session.commit()

      # seed meal data
      l1 = Log(
          meal_no=1,
          date=datetime.strptime("2022-02-01", "%Y-%m-%d"),
          user_id=u1.id
      )
      db.session.add_all([l1])
      self.l1 = l1
      db.session.commit()

      # seed food item data
      i1 = FoodItem(
          name="chicken breast",
          sugar_gram = 0,
          fiber_gram = 0,
          serving_size_gram = 200,
          sodium_mg = 145,
          potassium_mg = 453,
          fat_saturation_gram = 2,
          fat_total_gram = 7.1,
          calories = 332.5,
          cholesterol_mg = 171,
          protein_gram = 61.9,
          carbohydrate_gram = 0,
          log_id=l1.id
      )

      i2 = FoodItem(
          name="onion",
          sugar_gram = 13.3,
          fiber_gram = 4,
          serving_size_gram = 283.495,
          sodium_mg = 8,
          potassium_mg = 99,
          fat_saturation_gram = 0.1,
          fat_total_gram = 0.5,
          calories = 126.7,
          cholesterol_mg = 0,
          protein_gram = 3.9,
          carbohydrate_gram = 28.6,
          log_id=l1.id
      )

      db.session.add_all([i1, i2])
      self.i1 = i1
      self.i2 = i2
      db.session.commit()


    def tearDown(self):
      """Clean up fouled transactions."""

      db.session.rollback()


    def test_search_all_meals_logged_by_date(self) -> None:
      '''
      Test GET /api/log/search
      Test that the routes returns json data of all meals logged for the given date.
      '''

      # arrange
      log_id = self.l1.id
      food_item_1_id = self.i1.id
      food_item_2_id = self.i2.id

      # act
      with app.test_client() as client:
        with client.session_transaction() as session:
          session[CURRENT_USER] = self.u1.id

      res = client.get("/api/log/search", query_string={'date': '2022-02-01'})
      data = res.json

      # assert
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data, 
      {
        "meals_logged": [
          {
            "date": "2022-02-01",
            "food_items": [
              {
                "calories": 332.5,
                "carbohydrate_gram": 0.0,
                "cholesterol_mg": 171,
                "fat_saturation_gram": 2.0,
                "fat_total_gram": 7.1,
                "fiber_gram": 0.0,
                "id": food_item_1_id,
                "name": "chicken breast",
                "potassium_mg": 453.0,
                "protein_gram": 61.9,
                "serving_size_gram": 200.0,
                "sodium_mg": 145.0,
                "sugar_gram": 0.0
              },
              {
                "calories": 126.7,
                "carbohydrate_gram": 28.6,
                "cholesterol_mg": 0.0,
                "fat_saturation_gram": 0.1,
                "fat_total_gram": 0.5,
                "fiber_gram": 4.0,
                "id": food_item_2_id,
                "name": "onion",
                "potassium_mg": 99.0,
                "protein_gram": 3.9,
                "serving_size_gram": 283.495,
                "sodium_mg": 8.0,
                "sugar_gram": 13.3
              }
            ],
            "id": log_id,
            "meal_no": 1,
            "user_id": self.u1.id
          }
        ]
      })
      

    def test_log_a_new_meal(self) -> None:
      '''
      Test POST /api/log/new
      Test that the route log a new meal in db and returns json data of the meal logged
      '''

      # arrange
      payload = {
        "meal_no": 2,
        "food_items": [
          {
            'name': 'white rice',
            'sugar': 0.1,
            'fiber': 0.4,
            'servingSize': 100.0,
            'sodium': 0.0,
            'potassium': 43.0,
            'saturatedFat': 0.1,
            'totalFat': 0.3,
            'calories': 132.0, 
            'cholesterol': 0.0, 
            'protein': 2.7, 
            'carbohydrate': 28.5
            }],
        "date_string": "2022-02-01"
      }

      # act
      with app.test_client() as client:
        with client.session_transaction() as session:
          session[CURRENT_USER] = self.u1.id
        
        res = client.post("/api/log/new", json=payload)
        data = res.json
        # delele log id and food item id because we don't know the exact value
        del data['log']['id']
        del data['log']['food_items'][0]['id']

        # assert
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data, {
          'log': {
              'date': '2022-02-01', 
              'food_items': [
                {
                  "calories": 132.0,
                  "carbohydrate_gram": 28.5,
                  "cholesterol_mg": 0.0,
                  "fat_saturation_gram": 0.1,
                  "fat_total_gram": 0.3,
                  "fiber_gram": 0.4,
                  "name": "white rice",
                  "potassium_mg": 43.0,
                  "protein_gram": 2.7,
                  "serving_size_gram": 100.0,
                  "sodium_mg": 0.0,
                  "sugar_gram": 0.1
                }
              ], 
              'meal_no': 2, 
              'user_id': self.u1.id
          }
        })

      
    def test_update_a_logged_meal(self) -> None:
      '''
      Test PATCH /api/log/update
      Test that the route updates the food item log id -> reassign the food item to another log
      '''

      # arrange  
      # move food item 1 from meal 1 to 2
      payload = {
        "meal_no": 2,
        "updated_item_id": self.i1.id,
        "date_string": "2022-02-01"
      }

      # act
      with app.test_client() as client:
        with client.session_transaction() as session:
          session[CURRENT_USER] = self.u1.id
        
      res = client.patch('/api/log/update', json=payload)
      data = res.json
      # delele log id and food item id because we don't know the exact value
      del data['log']['id']
      del data['log']['food_items'][0]['id']

      # assert
      self.assertEqual(res.status_code, 201)
      self.assertEqual(data, {
        "log": {
          "date": "2022-02-01",
          "food_items": [
            {
              "calories": 332.5,
              "carbohydrate_gram": 0.0,
              "cholesterol_mg": 171.0,
              "fat_saturation_gram": 2.0,
              "fat_total_gram": 7.1,
              "fiber_gram": 0.0,
              "name": "chicken breast",
              "potassium_mg": 453.0,
              "protein_gram": 61.9,
              "serving_size_gram": 200.0,
              "sodium_mg": 145.0,
              "sugar_gram": 0.0
            }
          ],
          "meal_no": 2,
          "user_id": 1
        }
      })