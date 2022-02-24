<h1 align="center">Macronizer</h1>
<p align="center">An exciting and minimalistic food diary and macro tracking app!</p>
<p align="center"><a href="https://macronizer-app.herokuapp.com">Project Demo</a></p>

## About the Project

This app is an all-in-one solution for nutrition tracking including food logging and nutrients tracking.

Users can create their own account and profile. Once logged in with your account credentials, users can then search for food using natural language, and the app will return a list of items with the according quantity and nutrients information. Users will also be able to log the results into their diary.

All food diary can also be reviewed by selecting the date of entry.

## Getting Started

**Prerequisites**

- Python 3.8
- Pip
- npm
- PostgreSQL

**Installation**

1. Obtain a free API key from [CalorieNinjas API](https://calorieninjas.com/)
2. Clone the repo
   `git clone https://github.com/triethuynh2301/macronizer-app`
3. Create a virtual environment using venv
   `python3 -m venv venv`
   `source venv/bin/activate`
   then install dependencies into the virtual environment
   `pip install -r requirements.txt`
4. Create a .env file in root directory to specify environment variables, for example:

   ```
   SECRET_KEY=<YOUR_SECRET_KEY>
   FLASK_APP=macronizer.py
   FLASK_ENV=development

   # API key
   CALORIES_NINJA_API_KEY=<YOUR_API_KEY_FROM_STEP_1>

   # db
   DEV_DB_URL=postgresql:///macronizer_db
   TEST_DB_URL=postgresql:///macronizer_test_db
   ```

5. In step 4, the DEV_DB_URL and TEST_DB_URL is not yet created. So, we need to create a development db and test db (for testing purposes only).

   ```
   <!-- Connect to PostgresSQL under your username -->
   psql -U <YOUR_USERNAME>

   <!-- Create db for development -->
   user=# CREATE DATABASE macronizer_db;

   <!-- Create db to run unit and integration tests-->
   user=# CREATE DATABASE macronizer_test_db
   ```
6. Now that we have the databases, you can run the `seed.py` file to create the tables.

7. In the root directory, type `flask run` to run the app in development mode then open `localhost:5000` on browser to demo the app.

## Usage

1. Users can pick a date then search for food using natural language and log the items in diary.
   <img src="https://drive.google.com/uc?export=view&id=1iSrmw30JFHL-sjGIHVzBAGLEwqA1uvo8" style="width: 70%">

2. Users can drag and drop food items to update the diary or delete food from the diary.
   ![image](https://drive.google.com/uc?export=view&id=10cOfNI5166IR9e1FGhORa5_pqIPIwSfs)

## License

Distributed under the MIT license. See `LICENSE.txt` for more information.

## Acknowledgments

:star: [Bootstrap 5](https://getbootstrap.com/) <br>
:star: [Bootstrap Themes and Templates](https://bootstrapmade.com/) <br>
:star: [Font Awesome](https://fontawesome.com/) <br>
:star: [Vanilla JS DatePicker Component](https://mymth.github.io/vanillajs-datepicker/#/) <br>
:star: [CalorieNinjas API](https://calorieninjas.com/) <br>

## Contact

Triet Huynh - triethuynh2301@gmail.com
