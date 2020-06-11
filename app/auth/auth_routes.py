from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.auth import auth_bp
from app.database import User
from app.global_util import strip_text
from app.auth.forms import LoginForm
from app.constants import user_keys, db_collections
from app import login_manager

#Constants. The most used keys used to make a db query

USER_COLLECTION = db_collections[0]
USERNAME = user_keys[1]
USER_ID = user_keys[0]
USER_PASSWORD = user_keys[2]
USER_EMAIL = user_keys[4]
USER_ROLES = user_keys[3]



@login_manager.user_loader
def load_user(username):
    """Flask will try to load a user before every request by calling get_id method
    from the User class on it and feeding the return value to this function.
    If the username returned from Flask is valid the user will be loaded."""

    user = User.find_user(username_val=username)

    if not user:

        return None

    return User(username=user[USERNAME], password=user[USER_PASSWORD],
                email=[USER_EMAIL], roles=user[USER_ROLES], _id=user[USER_ID])


@auth_bp.route("/login", methods=("POST", "GET"), endpoint="login")
def login():

    """checks to see if the user is already authenticated or not. If not
    the user will input their username and password and if it matches they will be stored
    in flask-login so they can be authenticated. It also checks to see which role the user
    is and directs them to the appropriate homepage"""

    if current_user.is_authenticated:

        user = User.find_user(username_val=current_user.username)

        path = User.check_roles(user)

        return redirect(path)

    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":

        raw_username = request.form.get("username")
        username = strip_text(raw_username, toStr=True)  
        user = User.find_user(username_val=username) 

        raw_password = request.form.get("password")
        password = strip_text(raw_password, toStr=True)

        if user and User.check_pass(user[USER_PASSWORD], password):

            user_obj = User(username=user[USERNAME], password=user[USER_PASSWORD],
                email=[USER_EMAIL], roles=user[USER_ROLES], _id=user[USER_ID])

            login_user(user_obj)

            newpath = User.check_roles(user)

            print(newpath)

            return redirect(newpath)

        else:
            error = "Username or Password was incorrect."

            return render_template('auth/login.html', title='Sign In', form=form, error=error)

    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/logout', endpoint="logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for('base.home'))
