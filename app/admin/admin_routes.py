from flask import render_template, redirect, request, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.admin.forms import SearchForm, UserEditForm, CreateUser, CreateWorker, UserPasswordForm, EditForm, StorageFees
from app.admin import admin_bp
from app.database import User, MetaOps, AllInvOps
from app.admin.admin_util import search_method
from app.global_util import user_has_role, strip_text
from app.constants import meta_keys, user_keys,\
     userinv_keys, SEARCH_KEY, NULLVALUE
#from app import bootstrap

#Meta collection keys
SHIPMENT_NUM_METAKEY = meta_keys[2]
TAG_NUM_METAKEY = meta_keys[3]
DESIGNERS_METAKEY = meta_keys[4]
USER_ID_METAKEY = meta_keys[5]
EDITABLE_FIELDS_METAKEY = meta_keys[6]
STORAGE_PRICE_METAKEY = meta_keys[7]
#User inventory collection keys
TAG_NUM_USERINVKEY = userinv_keys[0]
SHIPMENT_NUM_USERINVKEY = userinv_keys[1]
DESIGNER_USERINVKEY = userinv_keys[2]
CLIENT_USERINVKEY = userinv_keys[3]
VOLUME_USERINVKEY = userinv_keys[4]
DATE_ENTERED_USERINVKEY = userinv_keys[5]
IMAGE_NUM_USERINVKEY = userinv_keys[6]
DESCRIPTION_USERINVKEY = userinv_keys[7]
LOCATION_USERINVKEY = userinv_keys[8]
STORAGE_FEES_USERINVKEY = userinv_keys[9]
PAID_LAST_USERINVKEY = userinv_keys[10]
#User collection keys
USERNAME_USERKEY = user_keys[1]
USER_ID_USERKEY = user_keys[0]
USER_PASSWORD_USERKEY = user_keys[2]
USER_EMAIL_USERKEY = user_keys[4]
USER_ROLES_USERKEY = user_keys[3]
USER_CLIENT_USERKEY = user_keys[5]



@admin_bp.route("/", methods=("GET", "POST"), endpoint="admin_home")
@admin_bp.route("/home", methods=("GET", "POST"), endpoint="admin_home")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_home():

    """If a user has the admin role they are directed here"""

    return render_template("admin/home.html")


@admin_bp.route("/search", methods=("GET", "POST"), endpoint="admin_search")
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

    designer_list = MetaOps.find_one(DESIGNERS_METAKEY)
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))
    form.client.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        designer = form.designer.data
        client = form.client.data

        data_dict = {TAG_NUM_USERINVKEY : tag_num,
        SHIPMENT_NUM_USERINVKEY : shipment_num,
        DESIGNER_USERINVKEY : designer, CLIENT_USERINVKEY : client}

        new_dict = search_method(data_dict)

        json_dict = json.dumps(new_dict)

        return redirect(url_for("admin.admin_edit", data=json_dict))

    return render_template("admin/search.html", form=form)


@admin_bp.route("/search/<designer>", endpoint="chosen_designer")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def chosen_designer(designer):

    """This func works with the admin_search function and the javascript n search.html.
    In search.html, when a designerfrom the designer dropdown list is selected
    the javascript in search.html picks up thedesigner and fetches this url /admin/search + designer.
    With the designer name this func is able to query the database and grab the clients associated with
    it. This func then jsons the db response and returns it so the js can grab it unjson it
    and add the client names to the selectfield."""

    client_list = User.find_user(username_val=designer, retval=USER_CLIENT_USERKEY)

    if client_list is None:

        return jsonify({"clients": [NULLVALUE[0]]})

    else:

        client_list.insert(0, NULLVALUE[0])

        return jsonify({"clients": client_list})


@admin_bp.route("/edit", methods=("GET", "POST"), endpoint="admin_edit")
@login_required
@user_has_role(user=current_user, required_roles=("admin"))
def admin_edit():

    """"""

    json_data = json.loads(request.args["data"])
    db_data = AllInvOps.find_all(json_data)

    form = EditForm()
    form.choices.choices = db_data

    designer_list = MetaOps.find_one(DESIGNERS_METAKEY)
    form.designer.choices = [(designer, designer) for designer in designer_list]
    
    client_list = User.find_user(username_val=designer_list[0], retval=USER_CLIENT_USERKEY)
    form.client.choices = [(client, client) for client in client_list]

    if form.validate_on_submit():

        if form.move.data:
            print("moving")
            designer = form.designer.data

            client = form.client.data

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            AllInvOps.update_all(tagnum_list, mainkey=TAG_NUM_USERINVKEY,
            update_keys=(DESIGNER_USERINVKEY, CLIENT_USERINVKEY), 
            update_vals=(designer, client))

            return redirect(url_for("admin.admin_search"))

        if form.delete.data:

            data = request.form.getlist("inv-data")

            tagnum_list = strip_text(data, turnto_int=True)

            AllInvOps.delete_all(tagnum_list, keytodel=TAG_NUM_USERINVKEY)

            return redirect(url_for("admin.admin_search"))

    return render_template("admin/edit.html", form=form, dbkeys=userinv_keys)


# @admin_bp.route("/admin/edit/<designer>", methods=("GET", "POST"), endpoint="fill_client_field")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def fill_client_field(designer):

#     js_Array = []

#     meta_data = db["Users"].find_one({"username": designer})

#     client_list = meta_data["clients"]

#     for client in client_list:

#         js_Array.append(client)

#     return jsonify({"clients": js_Array})


# @admin_bp.route("/admin/manage-users", methods=("GET", "POST"), endpoint="admin_manage_users")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_manage_users():

#     """This page diplays all the current users and allows for multiple operations to be done on their
#     info. """

#     form = UserEditForm()

#     user_list = list(db["Users"].find({}))

#     meta_list = db["MetaData"].find_one({"Name": "User Ids"})

#     editable_list = meta_list["Editable Fields"]

#     form.choices.choices = [(row['_id'], (row["username"],
#                                            row["email"],
#                                            row["roles"])) for row in user_list]

#     form.editable_fields.choices = [(field, field) for field in editable_list]

#     first_message = "Select Only One User."

#     title = "All Current Users"

#     if form.validate_on_submit() and request.method == "POST":

#         data = request.form.getlist("user-data")

#         if len(data) == 1:

#             userid_list = strip_text(data, turnto_int=True)

#             if request.form["bsubmit"] == "Remove User":

#                 username = find_user(user_list, "username", userid_list)

#                 remove_single_row(userid_list, "_id", db)

#                 remove_user("Designers", username, "MetaData", db, delfromArray=True)

#                 remove_user("Designer", username, "AllInv", db)

#                 message = "User was Removed"

#                 return render_template("admin/manage_users.html", form=form, message=message, title=title)

#             if request.form["bsubmit"] == "Change User Info":

#                 fieldto_edit = form.editable_fields.data

#                 newfield_val = form.change_to.data

#                 update_single_field(userid_list, "_id", fieldto_edit,
#                                     newfield_val, db, array=False)

#                 message = "User Info was Changed Successfully"

#                 return render_template("admin/manage_users.html", form=form, message=message, title=title)

#             if request.form["bsubmit"] == "Change Role To":

#                 new_role = form.roles.data

#                 update_single_field(userid_list, "_id", "roles", new_role, db, array=True)

#                 message = "Role Change was Successful"

#                 return render_template("admin/manage_users.html", form=form, message=message, title=title)

#             if request.form["bsubmit"] == "Change Password":

#                 if len(userid_list) > 0:

#                     return redirect(url_for(".admin_user_password", userid=userid_list[0]))

#                 else:

#                     message = "Must Select a User before you can change their password!!"

#                     return render_template("admin/manage_users.html", form=form, message=message, title=title)

#             if request.form["bsubmit"] == "Add Client":

#                 new_client = form.add_client.data.upper()

#                 if validate_client(userid_list, new_client, db):

#                     update_single_field(userid_list, "_id", "clients", new_client, db,
#                                         array=True, save_array=True)

#                     message = "Client was Added Successfully"

#                     return render_template("admin/manage_users.html", form=form, message=message, title=title)

#                 else:

#                     message = "Client Already Exists or Selected User does not have the role of user."

#                     return render_template("admin/manage_users.html", form=form, message=message, title=title)
#         else:

#             form.choices.errors = "Select Only One User!!!"

#             return render_template("admin/manage_users.html", form=form)

#     return render_template("admin/manage_users.html", form=form, message=first_message, title=title, editable=editable_list)


# @admin_bp.route("/admin/change-password/<userid>", methods=("GET", "POST"), endpoint="admin_user_password")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_user_password(userid):

#     form = UserPasswordForm()

#     if form.validate_on_submit():

#         admin_password = form.admin_password.data

#         new_user_password = form.new_user_password.data

#         if validate_password(admin_password, current_user, db):

#             change_password(userid, new_user_password, db)

#             return redirect(url_for(".admin_manage_users"))

#         else:

#             form.admin_password.errors = "Current Admin Password was incorrect!!!"

#             return render_template("admin/change-user-password.html", form=form)

#     return render_template("admin/change-user-password.html", form=form)


# @admin_bp.route("/admin/create-worker", methods=("GET", "POST"), endpoint="admin_create_worker")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_create_worker():

#     form = CreateWorker()

#     if form.validate_on_submit():

#         username = form.username.data

#         if validate_username(username, db):

#             password = form.password.data

#             email = form.email.data

#             role = form.roles.data

#             create_worker(username, password, email, role, db)

#             message = "Worker Created Successfully."

#             return render_template("admin/create-worker.html", form=form, message=message)

#         else:

#             message = "Username Already Exists."

#             return render_template("admin/create-worker.html", form=form, message=message)

#     return render_template("admin/create-worker.html", form=form)


# @admin_bp.route("/admin/create-user", methods=("GET", "POST"), endpoint="admin_create_user")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_create_user():

#     form = CreateUser()

#     title = "Create a New User"

#     message = "If there are multiple known clients, separate each one with a comma."

#     if form.validate_on_submit():

#         username = form.username.data

#         if validate_username(username, db):

#             password = form.password.data

#             email = form.email.data

#             clients = form.known_clients.data

#             client_list = clients.strip().upper().split(",")

#             create_user(username, password, email, client_list, db)

#             message = "User was Successfully Created."

#             return render_template("/admin/create-user.html", form=form, message=message, title=title)

#         else:

#             message = "Username Already Exists."

#             return render_template("/admin/create-user.html", form=form, message=message, title=title)

#     return render_template("/admin/create-user.html", form=form, title=title, message=message)


# @admin_bp.route("/admin/storage-fees", methods=("GET", "POST"), endpoint="admin_storage_fees")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_storage_fees():

#     meta_data = db["MetaData"].find_one({"Name": "Designer Info"})

#     designer_list = meta_data["Designers"]

#     form = StorageFees()

#     form.designers.choices = [(designer, designer) for designer in designer_list]

#     client_data = db["Users"].find_one({"username": designer_list[0]})

#     client_list = client_data['clients']

#     client_list.insert(0, "None")

#     form.clients.choices = [(client, client) for client in client_list]

#     if form.validate_on_submit():

#         designer = form.designers.data

#         client = form.clients.data

#         data = json.dumps({"Designer": designer, "Client": client})

#         return redirect(url_for(".admin_show_fees", data=data))

#     return render_template("admin/storage-fees.html", form=form)


# @admin_bp.route("/admin/show-fees", methods=("GET", "POST"), endpoint="admin_show_fees")
# @login_required
# @user_has_role(user=current_user, required_roles=("admin"))
# def admin_show_fees():

#     json_data = request.args["data"]

#     search_data = json.loads(json_data)


#     db_data, title = database_search(search_data, db)

#     title = "Current Storage Fees for " + title


#     show_data = [(row["_id"], row["Designer"], row["Client"], row['Date Entered'],
#                   row["Storage Fees"])
#                   for row in db_data]

#     return render_template("admin/show-fees.html", data=show_data, title=title)

