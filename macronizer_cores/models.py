from sqlalchemy import CheckConstraint
from macronizer_cores import db, bcrypt


# SECTION models
class User(db.Model):
    '''
    Model for User
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.Text,
                    nullable=False)
    email = db.Column(db.Text, 
                        nullable=False,
                        unique=True)
    username = db.Column(db.Text,
                            nullable=False,
                            unique=True)
    password = db.Column(db.Text, nullable=False)

    # relationship
    meals = db.relationship(
        "Log",
        backref="user",
        passive_deletes=True
    )

    # methods
    def __repr__(self):
        return f"<User #{self.id}: {self.name}>"
    
    @classmethod
    def register(cls, username: str, password: str):
        '''
        Hash password for user
        ----------------------------------------------------------------
        
        Parameters
        --------------
        username: str
            Username to register user
        password: str
            User's chosen password

        Returns
        --------------
        Tuple containing username and password
        '''

        # hash password and convert into UNICODE string
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        # return tuple contaning username and password
        return (username, hashed_pwd)

    @classmethod
    def authenticate(cls, username, password):
        '''
        Authenticate user
        ----------------------------------------------------------------

        Parameters
        --------------
        username: str
            Username to register user
        password: str
            User's chosen password

        Returns
        --------------
        If authentication succeeds, return User object
        Else, return false
        '''

        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def serialize(self):
        '''Seralize into dictionary'''

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
        }


class Log(db.Model):
    '''
    Model for log
    '''

    __tablename__ = 'meal_logs'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    meal_no = db.Column(db.Integer,
                            CheckConstraint("meal_no BETWEEN 1 AND 5 "),
                            nullable=False
                        )
    date = db.Column(db.Date, 
                        nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False
    )

    # relationship
    food_items = db.relationship(
        "FoodItem",
        backref="meal",
        passive_deletes=True
    )

    # method
    def serialize(self):
        '''
        Serialize into a dictionary (JSON representation)
        '''

        return {
            "id": self.id,
            "meal_no": self.meal_no,
            "date": self.date.strftime("%Y-%m-%d"),
            "user_id": self.user_id,
            "food_items": [item.serialize() for item in self.food_items]
        }


class FoodItem(db.Model):
    '''
    Model for nutrition information
    '''

    __tablename__ = 'food_items'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(db.Text, nullable=False)
    sugar_gram = db.Column(db.Float, nullable=False)
    fiber_gram = db.Column(db.Float, nullable=False)
    serving_size_gram = db.Column(db.Float, nullable=False)
    sodium_mg = db.Column(db.Float, nullable=False)
    potassium_mg = db.Column(db.Float, nullable=False)
    fat_saturation_gram = db.Column(db.Float, nullable=False)
    fat_total_gram = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    cholesterol_mg = db.Column(db.Float, nullable=False)
    protein_gram = db.Column(db.Float, nullable=False)
    carbohydrate_gram = db.Column(db.Float, nullable=False)

    # relationship
    log_id = db.Column(
        db.Integer,
        db.ForeignKey("meal_logs.id", ondelete="cascade"),
        nullable=False
    )

    # method
    def serialize(self):
        '''Serialize into dictionary'''

        return {
            "id": self.id,
            "name": self.name,
            "sugar_gram": self.sugar_gram,
            "fiber_gram": self.fiber_gram,
            "serving_size_gram": self.serving_size_gram,
            "sodium_mg": self.sodium_mg,
            "potassium_mg": self.potassium_mg,
            "fat_saturation_gram": self.fat_saturation_gram,
            "fat_total_gram": self.fat_total_gram,
            "calories": self.calories,
            "cholesterol_mg": self.cholesterol_mg,
            "protein_gram": self.protein_gram,
            "carbohydrate_gram": self.carbohydrate_gram
        }
    
