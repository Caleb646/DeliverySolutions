from flask import render_template, redirect, request, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.user.forms import UserSearch, StorageFeesSearch
from app.user import user_bp
from app.database import User, MetaOps, AllInvOps, SortingOps
from app.user.user_util import search_method
from app.global_util import user_has_role, strip_text
from app.constants import meta_keys, user_keys,\
     userinv_keys, sort_methods, SEARCH_KEY, NULLVALUE, SORTMETHOD_KEY

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
DELIVERED_USERINVKEY = userinv_keys[11]
DELIVERY_DATE_USERINVKEY = userinv_keys[12]
PAID_LAST_DATE_USERINVKEY = userinv_keys[13]
#User collection keys
USERNAME_USERKEY = user_keys[1]
USER_ID_USERKEY = user_keys[0]
USER_PASSWORD_USERKEY = user_keys[2]
USER_EMAIL_USERKEY = user_keys[4]
USER_ROLES_USERKEY = user_keys[3]
USER_CLIENT_USERKEY = user_keys[5]
#Sort Methods
SPECIFIC_CLIENT_SUM = sort_methods[0]
ALL_CLIENTS_SUM = sort_methods[1]
INDIVIDUAL_ITEMS = sort_methods[2]
#Routes for Sorting Methods
SORTMETHODS_DICT = {SPECIFIC_CLIENT_SUM: "specific_client_sum.html",
    ALL_CLIENTS_SUM: "all_clients_sum.html", INDIVIDUAL_ITEMS: "all_indiv_fees.html"}


@user_bp.route("/", methods=("GET", "POST"), endpoint="user_home")
@user_bp.route("/home", methods=("GET", "POST"), endpoint="user_home")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_home():
    return render_template("user/home.html")


@user_bp.route("/search", methods=("GET", "POST"), endpoint="user_search")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_search():

    client_list = User.find_user(username_val=current_user.username, retval=USER_CLIENT_USERKEY)

    form = UserSearch()
  
    form.client.choices = [(client, client) for client in client_list]

    form.client.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))

    if form.validate_on_submit():

        tag_num = form.tag_num.data
        shipment_num = form.shipment_num.data
        client = form.client.data

        data = {TAG_NUM_USERINVKEY: tag_num, 
        SHIPMENT_NUM_USERINVKEY: shipment_num, 
        DESIGNER_USERINVKEY: current_user.username,
         CLIENT_USERINVKEY: client}

        data_dict = search_method(data)

        json_dict = json.dumps(data_dict)

        return redirect(url_for("user.user_view", data=json_dict))

    return render_template("user/search.html", form=form)


@user_bp.route("/view", methods=("GET", "POST"), endpoint="user_view")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_view():

    json_data = request.args["data"]

    search_data = json.loads(json_data)

    database_data = AllInvOps.find_all(search_data)

    return render_template("user/view.html", data=database_data, dbkeys=userinv_keys)


@user_bp.route("/storage-fees", methods=("GET", "POST"), endpoint="user_storage_fees")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_storage_fees():

    form = StorageFeesSearch()

    client_list = User.find_user(username_val=current_user.username, retval=USER_CLIENT_USERKEY)

    form.clients.choices = [(client, client) for client in client_list]

    form.clients.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))

    if form.validate_on_submit():

        chosen_method = form.sort_methods.data

        chosen_client = form.clients.data

        data_dict = {SORTMETHOD_KEY:chosen_method,
        DESIGNER_USERINVKEY:current_user.username,
        CLIENT_USERINVKEY:chosen_client}

        json_dict = json.dumps(data_dict)
    

        return redirect(url_for("user.user_show_fees", data=json_dict))

    return render_template("user/storage-fees.html", form=form)


@user_bp.route("/show-fees", methods=("GET", "POST"), endpoint="user_show_fees")
@login_required
@user_has_role(user=current_user, required_roles=("user"))
def user_show_fees():

    json_dict = request.args["data"]

    data_dict = json.loads(json_dict)

    sort_method = data_dict.get(SORTMETHOD_KEY)

    client = data_dict.get(CLIENT_USERINVKEY)

    designer = data_dict.get(DESIGNER_USERINVKEY)

    title = "Storage Fees for: " + client if client not in NULLVALUE else "Storage Fees"

    db_data: dict = SortingOps.sorting_controller(sort_method, designer, client)

    #picks what template path to use
    sort_template = SORTMETHODS_DICT.get(sort_method)



    return render_template("user/"+sort_template, data=db_data, dbkeys=userinv_keys, title=title)
