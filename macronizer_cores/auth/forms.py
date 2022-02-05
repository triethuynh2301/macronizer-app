from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired("Username can't be empty")])
    password = PasswordField('Password', validators=[Length(min=6)])

class RegisterForm(FlaskForm):
    '''Register Form'''
    
    name= StringField(
        'Your Name',
        validators=[DataRequired("Name can't be empty")]
    )
    email= EmailField(
        'Email', 
        validators=[
            DataRequired("Email can't be empty"),
            Email("Invalid email address.")
        ]
    )
    username = StringField('Username', validators=[DataRequired("Username can't be empty")])
    password = PasswordField('Password', validators=[Length(min=6)])

