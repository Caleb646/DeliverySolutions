from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from flask_pymongo import PyMongo
from random import randint
from datetime import datetime
from app.constants import roles_routes, db_collections,\
     user_keys, meta_keys, userinv_keys
from app import ADMIN_PASS,\
     SUPEREMPLOYEE_PASS, EMPLOYEE_PASS, USER_PASS, db

#Collections
USER_COLLECTION = db_collections[0]
META_COLLECTION = db_collections[1]
#User collection keys
USERNAME_USERKEY = user_keys[1]
USER_ID_USERKEY = user_keys[0]
USER_PASSWORD_USERKEY = user_keys[2]
USER_EMAIL_USERKEY = user_keys[4]
USER_ROLES_USERKEY = user_keys[3]
USER_CLIENT_USERKEY = user_keys[5]
#Meta collection keys
META_ID_KEY = meta_keys[0]
META_ID_VALUE = meta_keys[1]
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
STORAGE_FEES_USERINVKEY = userinv_keys[9]
PAID_LAST_USERINVKEY = userinv_keys[10]


class MetaOps:

    @staticmethod
    def find_one(keyto_find):

        ret = db[META_COLLECTION].find_one({META_ID_KEY:META_ID_VALUE})

        return ret[keyto_find]


class User(UserMixin):

    """Creates a User obj to pass to flask_login.
    Also validates a user based on their given roles
    which are: user, admin, super_employee, employee"""

    def __init__(self, username, email, password, roles, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.roles = roles
        self._id = _id

    
    @staticmethod
    def find_user(username_val=None, userid_val=None, userid=False, retval=None):

        """Returns user obj using either the username or user id"""
        
        if not userid:

            user = db[USER_COLLECTION].find_one({USERNAME_USERKEY:username_val})

            if retval != None and user != None:

                return user[retval]

            else:

                return user
        
        else:

            user = db[USER_COLLECTION].find_one({USER_ID_USERKEY:userid_val})

            if retval != None and user != None:

                return user[retval]

            else:

                return user


    @staticmethod
    def check_pass(passwordin_db, passwordto_check):
        return check_password_hash(passwordin_db, passwordto_check)

    @staticmethod
    def check_roles(user):

        """Checks what role the authorized user has and then returns
        the appropriate template path"""

        route = roles_routes[user[USER_ROLES_USERKEY][0]]

        return route

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


def init_db():

    inv_size = 10

    starting_users = {"Joe": ["BOB", "JANE","CAT", "JILL","LEVI"], "Bill": ["CALEB","MADDIE", "CHARLIE"]}

    user_list_len = len(starting_users.keys()) - 1

    admin_input = input("Type y or n if data should be reentered: ")

    if admin_input == "y":

        Users = db[USER_COLLECTION]

        Users.insert_one({USER_ID_USERKEY: 1, USERNAME_USERKEY: "Caleb", USER_PASSWORD_USERKEY : generate_password_hash(ADMIN_PASS),
                          USER_ROLES_USERKEY : [ "admin" ], USER_EMAIL_USERKEY : "calebthomas646@yahoo.com" })

        Users.insert_one({USER_ID_USERKEY: 2, USERNAME_USERKEY: "Joe", USER_PASSWORD_USERKEY: generate_password_hash(USER_PASS),
                          USER_ROLES_USERKEY: ["user"], USER_EMAIL_USERKEY: "calebthomas646@yahoo.com",
                           USER_CLIENT_USERKEY: ["BOB", "JANE","CAT", "JILL","LEVI"]})

        Users.insert_one({USER_ID_USERKEY: 3, USERNAME_USERKEY: "Bill", USER_PASSWORD_USERKEY: generate_password_hash(USER_PASS),
                          USER_ROLES_USERKEY: ["user"], USER_EMAIL_USERKEY: "calebthomas646@yahoo.com",
                           USER_CLIENT_USERKEY: ["CALEB","MADDIE", "CHARLIE"]})

        Users.insert_one({USER_ID_USERKEY: 4, USERNAME_USERKEY: "Jill", USER_PASSWORD_USERKEY: generate_password_hash(SUPEREMPLOYEE_PASS),
                          USER_ROLES_USERKEY: ["super_employee"], USER_EMAIL_USERKEY: "calebthomas646@yahoo.com"})

        Users.insert_one({USER_ID_USERKEY: 5, USERNAME_USERKEY: "Jane", USER_PASSWORD_USERKEY: generate_password_hash(EMPLOYEE_PASS),
                          USER_ROLES_USERKEY: ["employee"], USER_EMAIL_USERKEY: "calebthomas646@yahoo.com"})

        metadata = db[META_COLLECTION]

        meta_list = {META_ID_KEY: META_ID_VALUE, SHIPMENT_NUM_METAKEY: inv_size*100, TAG_NUM_METAKEY: inv_size*100,
                    DESIGNERS_METAKEY: ["Joe", "Bill"],
                    USER_ID_METAKEY: 9, EDITABLE_FIELDS_METAKEY:["email",],
                    STORAGE_PRICE_METAKEY: .10}

        metadata.insert_one(meta_list)

        
        for i in range(user_list_len+1):

            designer_list = list(starting_users.keys())
            designer = designer_list[i]
            inv_data = []
            DB = db[designer]
            start_ind = i*inv_size

            for j in range(start_ind, inv_size+start_ind):

                print(j)

                clientList = starting_users[designer]

                listLen = len(clientList) - 1

                index = randint(0, listLen)

                client = clientList[index]

                data = {TAG_NUM_USERINVKEY: j, SHIPMENT_NUM_USERINVKEY: j,\
                DESIGNER_USERINVKEY: designer, CLIENT_USERINVKEY: client,\
                VOLUME_USERINVKEY :100,\
                DATE_ENTERED_USERINVKEY: datetime(2019, i+1, 20),\
                IMAGE_NUM_USERINVKEY: 1, DESCRIPTION_USERINVKEY: "A Table",\
                LOCATION_USERINVKEY: "A"+str(j),\
                STORAGE_FEES_USERINVKEY: 0, PAID_LAST_USERINVKEY: 0}

                inv_data.append(data)

            DB.insert_many(inv_data)
            inv_data.clear()



