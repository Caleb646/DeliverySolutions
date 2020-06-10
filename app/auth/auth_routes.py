from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.auth import auth_bp
from app.database import User
from app.auth.forms import LoginForm
from app import db, login_manager
import os


@login_manager.user_loader
def load_user(username):
    """This function looks at the User class in database.py and class the
    get_id method. Whatever is set to return for that method has to be the unique identifier
    for that user. It then takes the that identifier, calls the db and is the username
    exists in the db it will then return a User obj to Flask so that Flask_Login can monitor
    this user throughout."""

    user = db["Users"].find_one({"username": username})

    if not user:

        return None

    return User(username=user['username'], password=user["password"],
                email=["email"], roles=user["roles"], _id=user["_id"])


@auth_bp.route("/login", methods=("POST", "GET"), endpoint="login")
def login():

    """checks to see if the user is already authenticated or not. If not
    the user will input their username and password and if it matches they will be stored
    in flask-login so they can be authenticated. It also checks to see which role the user
    is and directs them to the appropriate homepage"""

    if current_user.is_authenticated:

        user = db.Users.find_one({"username": current_user.username})

        path = User.check_roles(user)

        return redirect(path)

    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":

        raw_username = request.form.get("username")
        username = strip_text(raw_username, toStr=True)    
        user = db.Users.find_one({"username": username})

        raw_password = request.form.get("password")
        password = strip_text(raw_password, toStr=True)

        if user and User.check_pass(user['password'], password):
            user_obj = User(username=user['username'], password=user["password"],
                    email=["email"], roles=user["roles"])
            login_user(user_obj)
            return redirect("/admin/home")

        else:
            error = "Username or Password was incorrect."

            return render_template('auth/login.html', title='Sign In', form=form, error=error)

    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/logout', endpoint="logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for('.home'))
