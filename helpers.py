from flask import redirect
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from re import sub


def database_search(data: dict, db):
    """The format of the json data sent
        to this function by /admin/search/ {"tag num": tag_num,
        "shipment num": shipment_num,
        "Designer": designer, "Client": client}.
        In the database, the tag num value is with the _id key.
        """
    db_data = None
    title = None

    print(data)

    if data["Designer"] is not "" and data["Designer"] != "None":

        if data["Client"] is not "" and data["Client"] != "None":
            db_data = list(db["AllInv"].find({"Designer": data["Designer"], "Client": data["Client"]}))
            title = data["Designer"] + "'s Current Inventory for" + " " + data["Client"]

        else:
            db_data = list(db["AllInv"].find({"Designer": data["Designer"]}))
            title = data["Designer"] + "'s Current Inventory"

    elif data["shipment num"] is not None and data["shipment num"] != "None":
        db_data = db["AllInv"].find_one({"shipment num": data["shipment num"]})
        if db_data is not None:
            title = "Shipment Number:" + " " + str(data["shipment num"])

        else:
            title = "Shipment Number:" + " " + str(data["shipment num"]) + " does not exist. Retry search!"

    elif data["tag num"] is not None and data["tag num"] != "None":
        db_data = db["AllInv"].find_one({"_id": data["tag num"]})

        if db_data is not None:
            title = "Tag Number:" + " " + str(data["tag num"])

        else:
            title = "Tag Number:" + " " + str(data["tag num"]) + "does not exist."

    else:
        db_data = list(db["AllInv"].find({}))
        title = "All Current Inventory"

    return db_data, title


def formatter(db_data):
    """db_data format: {'_id': 5.0, 'shipment_num': 4.0,
    'Designer': 'JONE', 'Client': 'JILL',
           'Volume': 100.0,
           'Date Entered': 'Date', 'Img Num': 12.0,
           'Description': 'A Table'}

           db_data list format: [{'_id': 5.0, 'shipment_num': 4.0,
    'Designer': 'JONE', 'Client': 'JILL',
           'Volume': 100.0,
           'Date Entered': 'Date', 'Img Num': 12.0,
           'Description': 'A Table'}]

           This func is responsible for formatting the database data so that it
           can be displayed on /admin/edit in a checkbox format. It takes the data
           and puts it into a tuple with the first element being the id and the second
           element being the rest of that specific items info. If db_data is None
           this func will return a tuple containing (None, None)"""

    data_list = []

    if db_data is not None:

        if type(db_data) is list:

            for row in db_data:
                data_list.append((row["_id"],
                                  (row['shipment num'],
                                   row['Designer'],
                                   row['Client'],
                                   row['Volume'],
                                   row['Date Entered'],
                                   row['Img Num'],
                                   row['Description'],
                                   row["Location"],
                                   row["Storage Fees"])))
        else:

            data_list.append((db_data["_id"],
                              (db_data['shipment num'],
                               db_data['Designer'],
                               db_data['Client'],
                               db_data['Volume'],
                               db_data['Date Entered'],
                               db_data['Img Num'],
                               db_data['Description'],
                               db_data["Location"],
                               db_data["Storage Fees"])))

        print(data_list)
        return data_list

    else:

        data_list = (None, None)

        return data_list


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


def strip_text(text: list, turnto_int=False):
    """Takes a list of tag numbers that along with additional chrs.
    These additional chrs are strip, the tag number is converted to an 
    integer and appended to a list which is then returned."""

    tagnum_list = []

    if turnto_int:

        for chr in text:
            stripped_text = int(sub("[() {}, ]", "", chr))

            print(stripped_text)

            tagnum_list.append(stripped_text)
    else:

        for chr in text:
            stripped_text = sub("[() {}, ]", "", chr)

            print(stripped_text)

            tagnum_list.append(stripped_text)

    return tagnum_list


def deleteby_tagnum(tag_nums: list, db):

    for num in tag_nums:

        db["AllInv"].remove({"_id": num})


def moveby_tagnum(designer, client, tagnum_list, db):

    for num in tagnum_list:

        db["AllInv"].update_one({"_id": num}, \
                                {"$set": {"Designer": designer, "Client": client}})


def remove_single_row(data_list: list, key, db):

    """Takes a list of values that along with the key will find the correct document in
    the db and delete it."""

    for data in data_list:

        db["Users"].remove({key: data})


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

                time_delta = tdys_date - date_paid_to

                print(f"time delta in else {time_delta}")
                print(f"days in else {time_delta.days}")

                storage_fees = time_delta.days * per_day_price

                db[allinv_tblname].update_one({"_id": row["_id"]},
                                              {"$set": {"Storage Fees": storage_fees, "Paid Last": tdys_date}})





