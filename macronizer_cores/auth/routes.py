from flask import session, render_template, redirect, flash, Blueprint, g
from macronizer_cores import db, CURRENT_USER
from macronizer_cores.models import User
from macronizer_cores.auth.forms import RegisterForm, LoginForm
from macronizer_cores.auth.utils import remove_user_from_session
from sqlalchemy.exc import IntegrityError
from datetime import datetime


# create auth blueprint
auth = Blueprint('auth', __name__)


# SECTION routes
# NOTE - before_app_request is executed before each request, even if outside of a blueprint.
@auth.before_app_request
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
@auth.after_app_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


@auth.route("/login", methods=["GET", "POST"])
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
    return render_template('auth/login.html', form=form)


@auth.route("/register", methods=["GET", "POST"])
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
    return render_template('auth/register.html', form=form)


# best practice to logout with POST request to prevent caching
@auth.route("/logout", methods=["POST"])
def logout():
    '''
    Log user out and redirect back to login page
    '''

    remove_user_from_session()
    flash("You have logged out.", "info")

    return redirect("/login")


