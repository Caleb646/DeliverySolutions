


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
            title = "Tag Number:" + " " + str(data["tag num"]) + " does not exist."

    else:
        db_data = list(db["AllInv"].find({}))
        title = "All Current Inventory"

    return db_data, title