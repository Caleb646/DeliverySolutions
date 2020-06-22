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