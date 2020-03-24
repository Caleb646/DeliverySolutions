from flask import url_for, render_template, request, flash, redirect, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from database import User, init_db
from forms import LoginForm, SearchForm
from run import *

#init_db()

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

    """checks to see if the user is already authenticated or not. If not
    the user will input their username and password and if it matches they will be stored
    in flask-login so they can be authenticated. It also checks to see which role the user
    is and directs them to the appropriate homepage"""

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

    """If a user has the admin role they are directed here"""

    return render_template("admin/home.html")


@app.route("/admin/search", methods=("GET", "POST"))
@login_required
def admin_search():

    """Allows the admin to search the database using either a designer/client name or
    tag/shipment number. This function renders the search.html which has two dropdown
    lists. The first, the designer list will be populated with names from the
    database upon the page being rendered. The client list will be populated once a
    designer is selected. This func works in tandem with chosen_designer. Once the form has
    been validated the results will be jsoned and the user will be redirected to the
    admin_edit func."""

    form = SearchForm()

    meta_data = mongo.db.MetaData.find_one({"Name": "Designer Info"})
    designer_list = meta_data["Designers"]
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(-1, ('Empty', 'Empty'))
    client_data = mongo.db.MetaData.find_one({"Name": form.designer.choices[0][1]})
    client_list = client_data["clients"]
    form.client.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        designer = form.designer.data
        client = form.client.data

        print(f'tag num, shipment num, designer, client {tag_num, shipment_num, designer, client}')

        data_dict = {"tag num": tag_num, "shipment num": shipment_num, "Designer": designer, "Client": client}

        json_dict = json.dumps(data_dict)

        return redirect(url_for(".admin_edit", data=json_dict))

    return render_template("admin/search.html", form=form)


@app.route("/admin/search/<designer>")
def chosen_designer(designer):

    """This func works with the admin_search function. In search.html, when a designer
    from the designer dropdown list is selected. The designer's name is sent to this function
    by means of the url <designer>. The database is then queried with that name and the
    results of that query are then jsonified where they are picked up a JavaScript script
    in search.html. The results are then used to populate the client dropdown list."""

    print(designer)
    js_Array = []
    print(js_Array)

    print(f"Designer is not equal to none: {designer}")
    meta_data = mongo.db.MetaData.find_one({"Name": designer})

    if meta_data is None:

        return jsonify({"clients": ["Empty"]})

    else:
        client_list = meta_data["clients"]

        for client in client_list:

            js_Array.append(client)

        js_Array.insert(-1, "Empty")

        return jsonify({"clients": js_Array})


@app.route("/admin/edit")
@login_required
def admin_edit():

#{"tag num": tag_num, "shipment num": shipment_num,
# "Designer": designer, "Client": client}

    json_data = request.args["data"]
    print(json_data)
    search_data = json.loads(json_data)
    print(f'search data {search_data}')

    return "It Worked"


"""Admin Views End"""


if __name__ == "__main__":
    app.run()