from flask import render_template, redirect, request, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.super_employee import super_employee_bp
from app.database import User, AllInvOps, MetaOps
from app.global_util import strip_text, user_has_role
from app.constants import meta_keys, user_keys,\
     userinv_keys, SEARCH_KEY, NULLVALUE
from app import login_manager
from app.super_employee.form import SearchForm
from app.super_employee.super_util import search_method

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
DUE_DATE_USERINVKEY = userinv_keys[9]
UNPAID_STORAGE_USERINVKEY = userinv_keys[10]
#User collection keys
USERNAME_USERKEY = user_keys[1]
USER_ID_USERKEY = user_keys[0]
USER_PASSWORD_USERKEY = user_keys[2]
USER_EMAIL_USERKEY = user_keys[4]
USER_ROLES_USERKEY = user_keys[3]
USER_CLIENT_USERKEY = user_keys[5]


@super_employee_bp.route("/home", methods=("GET",), endpoint="super_employee_home")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee"))
def super_employee_home():

    return render_template("super_employee/home.html")


@super_employee_bp.route("/search", methods=("GET", "POST"), endpoint="super_employee_search")
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
    designer_list = MetaOps.find_one(DESIGNERS_METAKEY)
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(0, (NULLVALUE[0], NULLVALUE[0],))
    form.client.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        designer = form.designer.data
        client = form.client.data

        data_dict = search_method({TAG_NUM_USERINVKEY:tag_num, SHIPMENT_NUM_USERINVKEY:shipment_num,
        DESIGNER_USERINVKEY:designer, CLIENT_USERINVKEY:client})

        json_dict = json.dumps(data_dict)

        return redirect(url_for("super_employee.super_employee_edit", data=json_dict))

    return render_template("super_employee/search.html", form=form)


# @app.route("/super_employee/edit", methods=("GET", "POST"), endpoint="super_employee_edit")
# @login_required
# @user_has_role(user=current_user, required_roles=("super_employee"))
# def super_employee_edit():
#     """The format of the json data sent
#     to this function by /admin/search/ {"tag num": tag_num,
#     "shipment num": shipment_num,
#     "Designer": designer, "Client": client}.
#     """

#     json_data = request.args["data"]
#     search_data = json.loads(json_data)

#     database_data, title = database_search(search_data, db)
#     formatted_data = formatter(database_data)

#     form = EditForm()
#     form.choices.choices = formatted_data

#     print(formatted_data)

#     meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
#     designer_list = meta_data["Designers"]
#     form.movetto_field.choices = [(designer, designer) for designer in designer_list]

#     client_data = db["Users"].find_one({"username": designer_list[0]})
#     client_list = client_data["clients"]
#     form.client.choices = [(client, client) for client in client_list]

#     if form.validate_on_submit():

#         if request.form["bsubmit"] == "Move To":
#             designer = form.movetto_field.data

#             client = form.client.data

#             data = request.form.getlist("inv-data")

#             tagnum_list = strip_text(data, turnto_int=True)

#             moveby_tagnum(designer, client, tagnum_list, db)

#             return redirect(url_for(".super_employee_search"))

#         if request.form["bsubmit"] == "Delete":

#             data = request.form.getlist("inv-data")

#             tagnum_list = strip_text(data, turnto_int=True)

#             deleteby_tagnum(tagnum_list, db)

#             return redirect(url_for(".super_employee_search"))

#     return render_template("super-employee/edit.html", form=form, title=title)



# @app.route("/super_employee/storage-fees", methods=("GET", "POST"), endpoint="super_employee_storage_fees")
# @login_required
# @user_has_role(user=current_user, required_roles=("super_employee"))
# def super_employee_storage_fees():

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

#         return redirect(url_for(".super_employee_show_fees", data=data))

#     return render_template("super-employee/storage-fees.html", form=form)


# @app.route("/super_employee/show-fees", methods=("GET", "POST"), endpoint="super_employee_show_fees")
# @login_required
# @user_has_role(user=current_user, required_roles=("super_employee"))
# def super_employee_show_fees():

#     json_data = request.args["data"]

#     search_data = json.loads(json_data)


#     db_data, title = database_search(search_data, db)

#     title = "Current Storage Fees for " + title


#     show_data = [(row["_id"], row["Designer"], row["Client"], row['Date Entered'],
#                   row["Storage Fees"])
#                   for row in db_data]

#     return render_template("super-employee/show-fees.html", data=show_data, title=title)

# @app.route("/super_employee/add-inv", methods=("GET", "POST"), endpoint="super_employee_add_inv")
# @login_required
# @user_has_role(user=current_user, required_roles=("super_employee"))
# def super_employee_add_inv():

#     form = AddForm()

#     meta_data = db["MetaData"].find_one({"Name": "Designer Info"})
#     designer_list = meta_data["Designers"]
#     form.designer.choices = [(designer, designer) for designer in designer_list]
#     form.designer.choices.insert(0, ('None', 'None'))
#     form.client.choices.insert(0, ('None', 'None'))

#     return render_template("super-employee/add-inv.html", form=form)


# @app.route("/super_employee/add-inv/success", methods=("GET", "POST"), endpoint="super_employee_add_inv_success")
# @login_required
# @user_has_role(user=current_user, required_roles=("super_employee"))
# def super_employee_add_inv_success():

#     """Grabs the entered data from the previous page and files it away 
#     into the database. The designer and client are located at the very
#     beginning of the first list. [[designer, client]] """

#     print("at success page")

#     rawdata_list = request.args.get("data")

#     print("data list", rawdata_list)

#     datalist = json.loads(rawdata_list)

#     user_list = datalist.pop(0)

#     enter_data(datalist, user_list, db)

#     return render_template("super-employee/add-inv-success.html", designer=user_list[0])
 

@super_employee_bp.route("/add-inv/<designer>", endpoint="chosen_designer_super_employee")
@login_required
@user_has_role(user=current_user, required_roles=("super_employee", "employee"))
def chosen_designer_super_employee(designer):

    """This func works with the admin_search function and the javascript n search.html.
    In search.html, when a designerfrom the designer dropdown list is selected
    the javascript in search.html picks up thedesigner and fetches this url /admin/search + designer.
    With the designer name this func is able to query the database and grab the clients associated with
    it. This func then jsons the db response and returns it so the js can grab it unjson it
    and add the client names to the selectfield."""

    js_Array = []

    client_list = User.find_user(username_val=designer, retval=CLIENT_USERINVKEY)

    print(client_list)

    if client_list is None:

        return jsonify({"clients": [NULLVALUE[0]]})

    else:

        client_list.insert(0, NULLVALUE[0])

        return jsonify({"clients": js_Array})