
def database_search(data: dict, db):
    """The format of the json data sent
        to this function by /admin/search/ {"tag num": tag_num,
        "shipment num": shipment_num,
        "Designer": designer, "Client": client}.
        """
    db_data = None
    title = None

    print(f'designer, client, shipment num, tag num: {data["Designer"],data["Client"],data["shipment num"],data["tag num"] }')
    print(len(data["Client"]) == 0, len(data["Client"]))
    if data["Designer"] is not "":

        if data["Client"] is not "":
            print("There was a client finding all of the designers inv")
            db_data = list(db[data["Designer"]].find({"Client": data["Client"]}))
            title = data["Designer"] + " " + data["Client"]

        else:
            print("There was no client finding all of the designers inv")
            db_data = list(db[data["Designer"]].find({}))
            title = data["Designer"]

    elif data["shipment num"] is not None:
        db_data = db["All Inv"].find_one({"shipment num": data["shipment num"]})
        title = data["shipment num"]

    elif data["tag num"] is not None:
        db_data = db["All Inv"].find_one({"tag num": data["tag num"]})
        title = data["tag num"]

    return db_data, title


def formatter(db_data):

    """db_data format: {'_id': 5.0, 'shipment_num': 4.0,
    'Designer': 'JONE', 'Client': 'JILL',
           'Volume': 100.0,
           'Date Entered': 'Date', 'Img Num': 12.0,
           'Description': 'A Table'}

           This func is responsible for formatting the database data say that it
           can be displayed on /admin/edit in a checkbox format. It the data
           and puts it into a tuple with the first element being the id and the second
           element being the rest of that specific items info"""

    data_list = []

    if type(db_data) is list:

        for row in db_data:

            data_list.append((row["_id"],
                              (row['shipment_num'],
                                row['Client'],
                                 row['Volume'],
                                  row['Date Entered'],
                                   row['Img Num'],
                                    row['Description'])))
    return data_list