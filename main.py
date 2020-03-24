from flask import url_for, render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from database import User
from forms import LoginForm, SearchForm
from run import *


login_manager.login_view = "login"
@login_manager.user_loader
def load_user(username):

    """This function looks at the User class in database.py and class the
    get_id method. Whatever is set to return for that method has to be the unique identifier
    for that user. It then takes the that identifier, calls the db and is the username
    exists in the db it will then return a User obj to Flask so that Flask_Login can monitor
    this user throughout."""

    user = mongo.db.Users.find_one({"username": username})
    print(f"user id and user: {username, user}")
    if not user:
        return None
    return User(username=user['username'], password=user["password"],
                email=["email"], roles=user["roles"])


@app.route("/")
@app.route("/home")
def home():
    form = LoginForm()
    return render_template("home.html", form=form)


@app.route("/login", methods=("POST", "GET"))
def login():
    print(current_user)
    if current_user.is_authenticated:
        user = mongo.db.Users.find_one({"username": current_user.username})
        path = User.check_roles(user)
        print(path)
        return redirect(path)

    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.Users.find_one({"username": form.login.data})
        if user and User.check_pass(user['password'], form.password.data):
            user_obj = User(username=user['username'], password=user["password"],
                    email=["email"], roles=user["roles"])
            login_user(user_obj)
            return redirect("/admin/home")

        else:
            error = "Username or Password was incorrect."
            return render_template('login.html', title='Sign In', form=form, error=error)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


"""Admin Views Start"""


@app.route("/admin", methods=("GET", "POST"))
@app.route("/admin/home", methods=("GET", "POST"))
@login_required
def admin_home():

    return render_template("admin/home.html")


@app.route("/admin/search", methods=("GET", "POST"))
@login_required
def admin_search():

    form = SearchForm()

    data = mongo.db.list_collection_names()
    print(data)
    for d in data:
        print(d)
    #meta_data = mongo.db.MetaData.find_one({"Name": "Designer Info"})
    #print(meta_data)
    #designer_list = meta_data["Designers"]
    #form.designer.choices = [designer for designer in designer_list]

    form.client.choices = []
    if form.validate_on_submit():
        #data = mongo.db.Users.find_one({"username": form.login.data})
        pass

    return render_template("admin/search.html", form=form)


"""Admin Views End"""


if __name__ == "__main__":
    app.run()