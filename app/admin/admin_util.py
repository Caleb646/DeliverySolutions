from app.constants import userinv_keys, SEARCH_KEY, NULLVALUE

#User inventory collection keys
TAG_NUM_USERINVKEY = userinv_keys[0]
SHIPMENT_NUM_USERINVKEY = userinv_keys[1]
DESIGNER_USERINVKEY = userinv_keys[2]
CLIENT_USERINVKEY = userinv_keys[3]


def search_method(data_dict: dict) -> dict:

    """Returns the dictionary with an added Search key for admin_edit to use"""

    designerVal = data_dict.get(DESIGNER_USERINVKEY)
    clientVal = data_dict.get(CLIENT_USERINVKEY)
    tagnumVal = data_dict.get(TAG_NUM_USERINVKEY)
    shipmentnumVal = data_dict.get(SHIPMENT_NUM_USERINVKEY)

    print(designerVal, clientVal, tagnumVal, shipmentnumVal)

    if designerVal not in NULLVALUE and clientVal not in NULLVALUE:

        print("designer and client were not None")

        data_dict[SEARCH_KEY] = (DESIGNER_USERINVKEY, CLIENT_USERINVKEY)

        return data_dict

    if designerVal not in NULLVALUE:
        
        data_dict[SEARCH_KEY] = (DESIGNER_USERINVKEY,)

        return data_dict

    if tagnumVal not in NULLVALUE:

        data_dict[SEARCH_KEY] = (TAG_NUM_USERINVKEY,)

        return data_dict
    
    if shipmentnumVal not in NULLVALUE:

        data_dict[SEARCH_KEY] = (SHIPMENT_NUM_USERINVKEY,)

        return data_dict

    else:

        data_dict[SEARCH_KEY] = (None,)

        return data_dict


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

        try:

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

            return data_list

        except KeyError as e:
            print(e)

    else:

        data_list = (None, None)

        return data_list