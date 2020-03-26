from flask import redirect
from functools import wraps

def database_search(data: dict, db):
    """The format of the json data sent
        to this function by /admin/search/ {"tag num": tag_num,
        "shipment num": shipment_num,
        "Designer": designer, "Client": client}.
        In the database, the tag num value is with the _id key.
        """
    db_data = None
    title = None


    print(f'designer, client, shipment num, tag num: {data["Designer"],data["Client"],data["shipment num"],data["tag num"] }')
    if data["Designer"] is not "" and data["Designer"] != "None":

        if data["Client"] is not "" and data["Client"] != "None":
            print("There was a client finding all of the designers inv")
            db_data = list(db["AllInv"].find({"Client": data["Client"]}))
            title = data["Designer"] + " " + data["Client"]

        else:
            print("There was no client finding all of the designers inv")
            db_data = list(db["AllInv"].find({"Designer": data["Designer"]}))
            title = "Designer:" + " " + data["Designer"]

    elif data["shipment num"] is not None and data["shipment num"] != "None":
        db_data = db["AllInv"].find_one({"shipment num": data["shipment num"]})
        if db_data is not None:
            title = "Shipment Number:" + " " + str(data["shipment num"])

        else:
            title = "Shipment Number:" + " " + str(data["shipment num"]) + " does not exist. Retry search!"

    elif data["tag num"] is not None and data["tag num"] != "None":
        print(data["tag num"])
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

                    return redirect("/"+role+"/home")

            return func(*args, **kwargs)

        return the_last_func

    return decorator

