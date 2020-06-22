from flask import render_template, redirect, request, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.employee import employee_bp
from app.database import User, AllInvOps, MetaOps
from app.global_util import strip_text, user_has_role
from app.constants import meta_keys, user_keys,\
     userinv_keys, SEARCH_KEY, NULLVALUE
from app import login_manager
from app.employee.forms import SearchForm, AddForm
from app.employee.employee_util import search_method

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



@employee_bp.route("/home", endpoint="employee_home")
@login_required
@user_has_role(user=current_user, required_roles=("employee"))
def employee_home():

   return render_template("employee/home.html")


@employee_bp.route("/add-inv", endpoint="employee_add_inv")
@login_required
@user_has_role(user=current_user, required_roles=("employee"))
def employee_add_inv():

    form = AddForm()
    designer_list = MetaOps.find_one(DESIGNERS_METAKEY)
    form.designer.choices = [(designer, designer) for designer in designer_list]
    form.designer.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))
    form.client.choices.insert(0, (NULLVALUE[0], NULLVALUE[0]))

    return render_template("employee/add-inv.html", form=form)


@employee_bp.route("/add-inv/success", methods=("GET", "POST"), endpoint="employee_add_inv_success")
@login_required
@user_has_role(user=current_user, required_roles=("employee"))
def employee_add_inv_success():

    """Grabs the entered data from the previous page and files it away 
    into the database. The designer and client are located at the very
    beginning of the first list. [[designer, client]] """

    rawdata_list = request.args.get("data")

    datalist = json.loads(rawdata_list)

    user_list = datalist.pop(0)

    AllInvOps.enter_all(data_list=datalist, users=user_list)

    return render_template("employee/add-inv-success.html", designer=user_list[0])


@employee_bp.route("/search", methods=("GET", "POST"), endpoint="employee_search")
@login_required
@user_has_role(user=current_user, required_roles=("employee"))
def employee_search():

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

        data_dict = search_method({TAG_NUM_USERINVKEY:tag_num, 
        SHIPMENT_NUM_USERINVKEY:shipment_num, DESIGNER_USERINVKEY:designer,
        CLIENT_USERINVKEY:client})

        json_dict = json.dumps(data_dict)

        return redirect(url_for("employee.employee_view", data=json_dict))

    return render_template("employee/search.html", form=form)


@employee_bp.route("/view", methods=("GET", "POST"), endpoint="employee_view")
@login_required
@user_has_role(user=current_user, required_roles=("employee"))
def employee_view():

    json_data = request.args["data"]

    search_data = AllInvOps.find_all(json.loads(json_data))

    return render_template("employee/view.html", data=search_data, dbkeys=userinv_keys)
