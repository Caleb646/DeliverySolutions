from flask import redirect
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from re import sub


def user_has_role(user, required_roles):
    """A decorator for views that not only need to check if the user is authenticated
    but also if the user has the required role to see the view. It takes flask's
    current_user as an argument and then a tuple of required_roles. If the user
    does not have the required role they are directed to a page that is suitable for
    the role they have. So someone with the role of user will be directed to
    /user/home."""

    def decorator(func):

        wraps(func)

        def the_last_func(*args, **kwargs):

            for role in user.roles:

                if role not in required_roles:
                    return redirect("/" + role + "/home")

            return func(*args, **kwargs)

        return the_last_func

    return decorator


def strip_text(text: list, turnto_int=False, toStr=False):
    """Takes a list of tag numbers that along with additional chrs.
    These additional chrs are strip, the tag number is converted to an 
    integer and appended to a list which is then returned."""

    tagnum_list = []

    wordInput = ""

    if turnto_int:

        for char in text:
            
            stripped_text = int(sub("[() {}, <> ]", "", char))

            tagnum_list.append(stripped_text)

    if toStr:

        for char in text:

            stripped_text = sub("[() {}, <> ]", "", char)

            wordInput += stripped_text

        return wordInput

            
    else:

        for char in text:

            stripped_text = sub("[() {}, <> ]", "", char)

            tagnum_list.append(stripped_text)

    return tagnum_list


def moveby_tagnum(designer, client, tagnum_list, db):

    for num in tagnum_list:

        db["AllInv"].update_one({"_id": num}, \
                                {"$set": {"Designer": designer, "Client": client}})


def remove_single_row(data_list: list, key, db):

    """Takes a list of values that along with the key will find the correct document in
    the db and delete it."""

    for data in data_list:

        db["Users"].remove({key: data})


def remove_user(keytofind, valuetodelete, table, db, delfromArray=False):

    if delfromArray:

        db[table].update( {keytofind:valuetodelete},
            {"$pull": {keytofind: {"$in":[valuetodelete]}}}
            )

    else:

        db[table].remove({keytofind:valuetodelete})


def find_user(userlist, keywanttofind, Uid=None):

    for row in userlist:
        
        if row["_id"] == Uid[0]:

            return row[keywanttofind]


def update_single_field(data_list: list, keytofind, keytoupdate, valuetoupdate, db, db_table="Users",\
                        array=False, save_array=False):

    """Takes a list of values that will be used along with the keytofind to find
    the correct document in the db. Then use the keytoupdate and valuetoupdate it
    will update that singular field. Right now can only be used with one valuetoupdate.
    This function will also update an array in the database using .$[] if array
    is set to True. Can also set the db_table name. It defaults to Users. The %push operator adds an element
    to an array without deleting the contents. $set deletes the contents."""

    if array:

        if save_array:

            for data in data_list:

                db[db_table].update_one({keytofind: data}, \
                        {"$push": {keytoupdate: valuetoupdate}})

        else:

            for data in data_list:

                db[db_table].update_one({keytofind: data}, \
                        {"$set": {keytoupdate+".$[]": valuetoupdate}})

    else:

        for data in data_list:

            db[db_table].update_one({keytofind: data}, \
                                   {"$set": {keytoupdate: valuetoupdate}})


def validate_password(pass_to_validate, current_user, db):

    currentuser_password = None

    current_user_data = db["Users"].find_one({"username": current_user.username})

    current_pass = current_user_data["password"]

    if check_password_hash(current_pass, pass_to_validate):

        return True


def change_password(user_id, new_password, db):

    db["Users"].update_one({"_id": user_id},
                           {"$set": {"password": generate_password_hash(new_password)}})


def validate_username(username, db):

    db_response = db["Users"].find_one({"username": username})

    if db_response is None:

        return True


def create_worker(username, password, email, role, db):

    hash_pass = generate_password_hash(password)

    meta_data = db["MetaData"].find_one({"Name": "User Ids"})

    current_id = meta_data['id']

    db["Users"].insert_one({"_id": current_id, "username": username, "password": hash_pass,
                           "email": email, "roles": [role]})

    current_id += 1

    update_single_field(["User Ids"], "Name", "id", current_id, db, array=False, db_table="MetaData")


def create_user(username, password, email, known_clients, db):

    hash_pass = generate_password_hash(password)

    meta_data = db["MetaData"].find_one({"Name": "User Ids"})

    current_id = meta_data['id']

    db["Users"].insert_one({"_id": current_id, "username": username, "password": hash_pass,
                            "email": email, "roles": ["user"], "clients": known_clients})

    db["MetaData"].update_one({"Name": "Designer Info"}, \
                                {"$push": {"Designers": username}})

    current_id += 1

    update_single_field(["User Ids"], "Name", "id", current_id, db, array=False, db_table="MetaData")


def validate_client(userid_list, clientto_add, db):

    designer_data = db["Users"].find_one({"_id": userid_list[0]})

    client_list = designer_data["clients"]

    print(f"client list {client_list}")

    if "user" not in designer_data["roles"] or clientto_add in client_list:

        return False

    else:

        return True


def calculate_storage_fees(db, allinv_tblname="AllInv", price_tblname="MetaData"):

    all_inv = db[allinv_tblname].find({})

    price_list = db[price_tblname].find_one({"Name": "Prices"})

    price = price_list["Storage Price"]

    tdys_date = datetime.today()

    user_input = input("Type y to continue: ")

    if user_input == "y":

        for row in all_inv:

            print(row)

            volume = row["Volume"]

            per_day_price = volume * price

            if row["Paid Last"] == "None":

                date_received = row["Date Entered"]

                time_delta = tdys_date - date_received

                print(f"time delta in if {time_delta}")
                print(f"days in if {time_delta.days}")

                storage_fees = time_delta.days * per_day_price

                print(f'storage fees {storage_fees}')

                db[allinv_tblname].update_one({"_id": row["_id"]},
                                       {"$set": {"Storage Fees": storage_fees, "Paid Last": tdys_date}})

            else:

                date_paid_to = row["Paid Last"]

                left_over_fees = row["Storage Fees"] if row["Storage Fees"] == None and "None" else 0

                time_delta = tdys_date - date_paid_to

                storage_fees = (time_delta.days * per_day_price) + left_over_fees

                db[allinv_tblname].update_one({"_id": row["_id"]},
                                              {"$set": {"Storage Fees": storage_fees, "Paid Last": tdys_date}})


def enter_data(data_list: list, user_list: list, db):

    table = "AllInv"
    metaTable = "MetaData"
    todays_date = datetime.today()
    keys = ["_id", "shipment num", "Designer", "Client", "Volume",
     "Description", "Location", "Img Num", "Date Entered", "Storage Fees",
     "Paid Last"]

    designer = user_list[0]
    client = user_list[1]

    metadata = db[metaTable].find_one({"Name": "Inv Data"})
    currentShipnum = metadata["shipment num"]
    currentTagnum = metadata["tag num"] + 5

    inv_data = []

    for data in data_list:
        
        data_dict = {keys[0]:currentTagnum, keys[1]:currentShipnum,
        keys[2]:designer, keys[3]:client, keys[4]:data[1], keys[5]:data[2],
        keys[6]: data[3], keys[7]:data[4], keys[8]: todays_date,
        keys[9]:0, keys[10]:None}

        inv_data.append(data_dict)

        currentShipnum += 1
        currentTagnum += 1

    metadata = db[metaTable].update_one({"Name": "Inv Data"},\
    {"$set": {"shipment num": currentShipnum, "tag num": currentTagnum}})

    db[table].insert_many(inv_data)





