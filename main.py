from flask import url_for, render_template, request, flash, redirect, jsonify, json
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from database import User, init_db
from forms import LoginForm, SearchForm, EditForm, UserEditForm, UserPasswordForm, CreateWorker,\
    CreateUser, StorageFees, UserSearch, AddForm
from helpers import database_search, formatter, user_has_role,\
    strip_text, deleteby_tagnum, moveby_tagnum, remove_single_row, update_single_field,\
    validate_password, change_password, validate_username, create_worker, create_user,\
    validate_client, calculate_storage_fees
from run import *

#init_db()

#calculate_storage_fees(db)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(username):

    """This function looks at the User class in database.py and class the
    get_id method. Whatever is set to return for that method has to be the unique identifier
    for that user. It then takes the that identifier, calls the db and is the username
    exists in the db it will then return a User obj to Flask so that Flask_Login can monitor
    this user throughout."""

    user = db["Users"].find_one({"username": username})
    print(f"user id and user: {username, user}")
    if not user:
        return None
    return User(username=user['username'], password=user["password"],
                email=["email"], roles=user["roles"], _id=user["_id"])


@app.route("/")
@app.route("/home", endpoint="home")
def home():
    form = LoginForm()
    return render_template("home.html", form=form)


@app.route("/login", methods=("POST", "GET"), endpoint="login")
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


@app.route('/logout', endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))


"""Admin Views Start"""


@app.route("/admin", methods=("GET", "POST"), endpoint="admin_home")
@app.route("/admin/home", methods=("GET", "POST"), endpoint="admin_home")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_home():

    """If a user has the admin role they are directed here"""

    return render_template("admin/home.html")


@app.route("/admin/search", methods=("GET", "POST"), endpoint="admin_search")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_search():

    """Allows the admin to search the database using either a designer/client name or
    tag/shipment number. This function renders the search.html which has two dropdown
    lists. The first, the designer list will be populated with names from the
    database upon the page being rendered. The client list will be populated once a
    designer is selected. This func works in tandem with chosen_designer. Once the form has
    been validated the results will be jsoned and the user will be redirected to the
    admin_edit func."""

    form = SearchForm()

    meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
    designer_list = meta_data["Designers"]
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(0, ('None', 'None'))
    form.client.choices.insert(0, ('None', 'None'))

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


@app.route("/admin/search/<designer>", endpoint="chosen_designer")
@login_required
@user_has_role(user=current_user, required_roles=("admin", "super_employee"))
def chosen_designer(designer):

    """This func works with the admin_search function and the javascript n search.html.
    In search.html, when a designerfrom the designer dropdown list is selected
    the javascript in search.html picks up thedesigner and fetches this url /admin/search + designer.
    With the designer name this func is able to query the database and grab the clients associated with
    it. This func then jsons the db response and returns it so the js can grab it unjson it
    and add the client names to the selectfield."""

    js_Array = []

    meta_data = db["Users"].find_one({"username": designer})

    if meta_data is None:

        return jsonify({"clients": ["None"]})

    else:
        client_list = meta_data["clients"]

        for client in client_list:

            js_Array.append(client)

        js_Array.insert(0, "None")

        return jsonify({"clients": js_Array})


@app.route("/admin/edit", methods=("GET", "POST"), endpoint="admin_edit")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_edit():

    """The format of the json data sent
    to this function by /admin/search/ {"tag num": tag_num,
    "shipment num": shipment_num,
    "Designer": designer, "Client": client}.
    """

    json_data = request.args["data"]
    print(json_data)
    search_data = json.loads(json_data)

    database_data, title= database_search(search_data, db)
    formatted_data = formatter(database_data)
    print(database_data, title)

    form = EditForm()
    form.choices.choices = formatted_data

    meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
    designer_list = meta_data["Designers"]
    form.movetto_field.choices = [(designer, designer) for designer in designer_list]
    
    client_data = db["Users"].find_one({"username": designer_list[0]})
    client_list = client_data["clients"]
    form.client.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        if request.form["bsubmit"] == "Move To":

            designer = form.movetto_field.data

            client = form.client.data

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            moveby_tagnum(designer, client, tagnum_list, db)

            return redirect(url_for(".admin_search"))

        if request.form["bsubmit"] == "Delete":

            print(request.form.getlist("inv-data"))

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            deleteby_tagnum(tagnum_list, db)

            return redirect(url_for(".admin_search"))

    return render_template("admin/edit.html", form=form, title=title)


@app.route("/admin/edit/<designer>", methods=("GET", "POST"), endpoint="fill_client_field")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def fill_client_field(designer):

    js_Array = []
    print(js_Array)

    print(f"Designer: {designer}")
    meta_data = db["Users"].find_one({"username": designer})

    client_list = meta_data["clients"]

    for client in client_list:

        js_Array.append(client)

    return jsonify({"clients": js_Array})


@app.route("/admin/manage-users", methods=("GET", "POST"), endpoint="admin_manage_users")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_manage_users():

    """This page diplays all the current users and allows for multiple operations to be done on their
    info. """

    form = UserEditForm()

    user_list = list(db["Users"].find({}))

    meta_list = db["MetaData"].find_one({"Name": "User Ids"})

    editable_list = meta_list["Editable Fields"]

    form.choices.choices = [(row['_id'], (row["username"],
                                           row["email"],
                                           row["roles"])) for row in user_list]

    form.editable_fields.choices = [(field, field) for field in editable_list]

    first_message = "Select Only One User."

    title = "All Current Users"

    if form.validate_on_submit():

        data = request.form.getlist("user-data")

        if len(data) == 1:

            userid_list = strip_text(data, turnto_int=True)

            if request.form["bsubmit"] == "Remove User":

                remove_single_row(userid_list, "username", db)

                message = "User was Removed"

                return render_template("admin/manage_users.html", form=form, message=message, title=title)

            if request.form["bsubmit"] == "Change User Info":

                fieldto_edit = form.editable_fields.data

                newfield_val = form.change_to.data

                update_single_field(userid_list, "_id", fieldto_edit,
                                    newfield_val, db, array=False)

                message = "User Info was Changed Successfully"

                return render_template("admin/manage_users.html", form=form, message=message, title=title)

            if request.form["bsubmit"] == "Change Role To":

                new_role = form.roles.data

                update_single_field(userid_list, "_id", "roles", new_role, db, array=True)

                message = "Role Change was Successful"

                return render_template("admin/manage_users.html", form=form, message=message, title=title)

            if request.form["bsubmit"] == "Change Password":

                if len(userid_list) > 0:

                    return redirect(url_for(".admin_user_password", userid=userid_list[0]))

                else:

                    message = "Must Select a User before you can change their password!!"

                    return render_template("admin/manage_users.html", form=form, message=message, title=title)

            if request.form["bsubmit"] == "Add Client":

                new_client = form.add_client.data.upper()

                if validate_client(userid_list, new_client, db):

                    update_single_field(userid_list, "_id", "clients", new_client, db,
                                        array=True, save_array=True)

                    message = "Client was Added Successfully"

                    return render_template("admin/manage_users.html", form=form, message=message, title=title)

                else:

                    message = "Client Already Exists or Selected User does not have the role of user."

                    return render_template("admin/manage_users.html", form=form, message=message, title=title)
        else:

            form.choices.errors = "Select Only One User!!!"

            return render_template("admin/manage_users.html", form=form)

    return render_template("admin/manage_users.html", form=form, message=first_message, title=title)


@app.route("/admin/change-password/<userid>", methods=("GET", "POST"), endpoint="admin_user_password")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_user_password(userid):

    form = UserPasswordForm()

    if form.validate_on_submit():

        admin_password = form.admin_password.data

        new_user_password = form.new_user_password.data

        if validate_password(admin_password, current_user, db):

            change_password(userid, new_user_password, db)

            return redirect(url_for(".admin_manage_users"))

        else:

            form.admin_password.errors = "Current Admin Password was incorrect!!!"

            return render_template("admin/change-user-password.html", form=form)

    return render_template("admin/change-user-password.html", form=form)


@app.route("/admin/create-worker", methods=("GET", "POST"), endpoint="admin_create_worker")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_create_worker():

    form = CreateWorker()

    if form.validate_on_submit():

        username = form.username.data

        if validate_username(username, db):

            password = form.password.data

            email = form.email.data

            role = form.roles.data

            create_worker(username, password, email, role, db)

            message = "Worker Created Successfully."

            return render_template("admin/create-worker.html", form=form, message=message)

        else:

            message = "Username Already Exists."

            return render_template("admin/create-worker.html", form=form, message=message)

    return render_template("admin/create-worker.html", form=form)


@app.route("/admin/create-user", methods=("GET", "POST"), endpoint="admin_create_user")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_create_user():

    form = CreateUser()

    title = "Create a New User"

    message = "If there are multiple known clients, separate each one with a comma."

    if form.validate_on_submit():

        username = form.username.data

        if validate_username(username, db):

            password = form.password.data

            email = form.email.data

            clients = form.known_clients.data

            client_list = clients.strip().upper().split(",")

            print(client_list)

            create_user(username, password, email, client_list, db)

            message = "User was Successfully Created."

            return render_template("/admin/create-user.html", form=form, message=message, title=title)

        else:

            message = "Username Already Exists."

            return render_template("/admin/create-user.html", form=form, message=message, title=title)

    return render_template("/admin/create-user.html", form=form, title=title, message=message)


@app.route("/admin/storage-fees", methods=("GET", "POST"), endpoint="admin_storage_fees")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_storage_fees():

    meta_data = db["MetaData"].find_one({"Name": "Designer Info"})

    print(meta_data)

    designer_list = meta_data["Designers"]
    print(designer_list)
    form = StorageFees()

    form.designers.choices = [(designer, designer) for designer in designer_list]

    client_data = db["Users"].find_one({"username": designer_list[0]})

    client_list = client_data['clients']

    client_list.insert(0, "None")

    form.clients.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        designer = form.designers.data

        client = form.clients.data

        data = json.dumps({"Designer": designer, "Client": client})

        return redirect(url_for(".admin_show_fees", data=data))

    return render_template("admin/storage-fees.html", form=form)


@app.route("/admin/show-fees", methods=("GET", "POST"), endpoint="admin_show_fees")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_show_fees():

    json_data = request.args["data"]

    search_data = json.loads(json_data)

    print(f'search data {search_data}')

    db_data, title = database_search(search_data, db)

    title = "Current Storage Fees for " + title

    print(db_data)

    show_data = [(row["_id"], row["Designer"], row["Client"], row['Date Entered'],
                  row["Storage Fees"])
                  for row in db_data]

    print(show_data)

    return render_template("admin/show-fees.html", data=show_data, title=title)

"""Admin Views End"""

"""User Views Start"""


@app.route("/user/home", methods=("GET", "POST"), endpoint="user_home")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_home():
    return render_template("user/home.html")


@app.route("/user/search", methods=("GET", "POST"), endpoint="user_search")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_search():

    currentuser_data = db["Users"].find_one({"_id": current_user._id})

    client_list = currentuser_data["clients"]

    form = UserSearch()

    form.client.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        client = form.client.data

        data_dict = {"tag num": tag_num, "shipment num": shipment_num, "Designer": current_user.username, "Client": client}

        json_dict = json.dumps(data_dict)

        return redirect(url_for(".user_view", data=json_dict))

    return render_template("user/search.html", form=form)


@app.route("/user/view", methods=("GET", "POST"), endpoint="user_view")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_view():

    json_data = request.args["data"]

    search_data = json.loads(json_data)

    database_data, title = database_search(search_data, db)

    return render_template("user/view.html", title=title, data=database_data)


@app.route("/user/storage-fees", methods=("GET", "POST"), endpoint="user_storage_fees")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_storage_fees():

    data_dict = {"Designer": current_user.username,
                 "Client": "None",
                 "tag num": "None",
                 "shipment num": "None"}

    database_data, title = database_search(data_dict, db)

    return render_template("user/view.html", title=title, data=database_data)


"""User Views End"""

"""Super Employee Views Start"""


@app.route("/super_employee/home", methods=("GET",), endpoint="super_employee_home")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee"))
def super_employee_home():

    return render_template("super-employee/home.html")


@app.route("/super_employee/search", methods=("GET", "POST"), endpoint="super_employee_search")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee"))
def super_employee_search():

    """Allows the admin to search the database using either a designer/client name or
    tag/shipment number. This function renders the search.html which has two dropdown
    lists. The first, the designer list will be populated with names from the
    database upon the page being rendered. The client list will be populated once a
    designer is selected. This func works in tandem with chosen_designer. Once the form has
    been validated the results will be jsoned and the user will be redirected to the
    admin_edit func."""

    form = SearchForm()

    meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
    designer_list = meta_data["Designers"]
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(0, ('None', 'None'))
    form.client.choices.insert(0, ('None', 'None'))

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        designer = form.designer.data
        client = form.client.data

        print(f'tag num, shipment num, designer, client {tag_num, shipment_num, designer, client}')

        data_dict = {"tag num": tag_num, "shipment num": shipment_num, "Designer": designer, "Client": client}

        json_dict = json.dumps(data_dict)

        return redirect(url_for(".super_employee_edit", data=json_dict))

    return render_template("super-employee/search.html", form=form)


@app.route("/super_employee/edit", methods=("GET", "POST"), endpoint="super_employee_edit")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee"))
def super_employee_edit():
    """The format of the json data sent
    to this function by /admin/search/ {"tag num": tag_num,
    "shipment num": shipment_num,
    "Designer": designer, "Client": client}.
    """

    json_data = request.args["data"]
    print(json_data)
    search_data = json.loads(json_data)

    database_data, title = database_search(search_data, db)
    formatted_data = formatter(database_data)
    print(database_data, title)

    form = EditForm()
    form.choices.choices = formatted_data

    meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
    designer_list = meta_data["Designers"]
    form.movetto_field.choices = [(designer, designer) for designer in designer_list]

    client_data = db["Users"].find_one({"username": designer_list[0]})
    client_list = client_data["clients"]
    form.client.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        if request.form["bsubmit"] == "Move To":
            designer = form.movetto_field.data

            client = form.client.data

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            moveby_tagnum(designer, client, tagnum_list, db)

            return redirect(url_for(".super_employee_search"))

        if request.form["bsubmit"] == "Delete":
            print(request.form.getlist("inv-data"))

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            deleteby_tagnum(tagnum_list, db)

            return redirect(url_for(".super_employee_search"))

    return render_template("super-employee/edit.html", form=form, title=title)

@app.route("/super_employee/add-inv", methods=("GET", "POST"), endpoint="super_employee_add_inv")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee"))
def super_employee_add_inv():

    form = AddForm()

    return render_template("super-employee/add-inv.html", form=form)


"""Super Employee Views End"""





if __name__ == "__main__":
    app.run()