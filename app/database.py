from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import uuid
from app import db, ADMIN_PASS, SUPEREMPLOYEE_PASS, EMPLOYEE_PASS, USER_PASS


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
    def check_pass(passwordin_db, passwordto_check):
        return check_password_hash(passwordin_db, passwordto_check)

    @staticmethod
    def check_roles(user):

        """Checks what role the authorized user has and then returns
        the appropriate template path"""

        if "admin" in user["roles"]:
            return "/admin/home"
        if "user" in user["roles"]:
            return "/user/home"
        if "super_employee" in user["roles"]:
            return "/super_employee/home"
        if "employee" in user["roles"]:
            return "/employee/home"

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

    admin_input = input("Type y or n if data should be reentered: ")

    if admin_input == "y":

        Users = db["Users"]

        Users.insert_one({"_id": 1, "username": "Caleb", "password" : generate_password_hash(ADMIN_PASS),
                          "roles" : [ "admin" ], "email" : "calebthomas646@yahoo.com" })
        Users.insert_one({"_id": 2, "username": "Joe", "password": generate_password_hash(USER_PASS),
                          "roles": ["user"], "email": "calebthomas646@yahoo.com",
                           "clients": ["BOB", "JANE","CAT", "JILL","LEVI"]})
        Users.insert_one({"_id": 3, "username": "Bill", "password": generate_password_hash(USER_PASS),
                          "roles": ["user"], "email": "calebthomas646@yahoo.com",
                           "clients": ["CALEB","MADDIE", "CHARLIE"]})
        Users.insert_one({"_id": 4, "username": "Jill", "password": generate_password_hash(SUPEREMPLOYEE_PASS),
                          "roles": ["super_employee"], "email": "calebthomas646@yahoo.com"})
        Users.insert_one({"_id": 5, "username": "Jane", "password": generate_password_hash(EMPLOYEE_PASS),
                          "roles": ["employee"], "email": "calebthomas646@yahoo.com"})

        # Users.insert_one({"_id": 5, "username": "John", "password": generate_password_hash('Anna'),
        #                   "roles": ["user"], "email": "calebthomas646@yahoo.com",
        #                   "clients": ["BOB", "JANE"]})
        # Users.insert_one({"_id": 6, "username": "Paul", "password": generate_password_hash('Anna'),
        #                   "roles": ["user"], "email": "calebthomas646@yahoo.com",
        #                   "clients": [,"CAT", "JILL"]})
        # Users.insert_one({"_id": 7, "username": "Mary", "password": generate_password_hash('Anna'),
        #                   "roles": ["user"], "email": "calebthomas646@yahoo.com",
        #                   "clients": ["LEVI", "CALEB"]})
        # Users.insert_one({"_id": 8, "username": "Jone", "password": generate_password_hash('Anna'),
        #                   "roles": ["user"], "email": "calebthomas646@yahoo.com",
        #                   "clients": ["MADDIE", "CHARLIE"]})

        metadata = db["MetaData"]

        meta_list = [{'Name': "Inv Data", "shipment num": 10, "tag num": 10},
                    {'Name': "Designer Info", "Designers": ["Joe", "Bill"]},
                     {"Name": "User Ids", "id": 9, "Editable Fields":["email",]},
                     {"Name": "Prices", "Storage Price": .10}]

        metadata.insert_many(meta_list)

        all_inv = db["AllInv"]

        inv_data = [{"_id": 1, "shipment num": 1, 'Designer': "Joe",\
                    "Client": "BOB", "Volume":100, "Date Entered": datetime(2019, 5, 20),\
                     "Img Num": 1, "Description": "A Table", "Location": "A4",
                     "Storage Fees": "None", "Paid Last": "None"},
                    {"_id": 2, "shipment num": 2, 'Designer': "Joe", \
                     "Client": "JILL", "Volume": 100, "Date Entered": datetime(2019, 5, 10), \
                     "Img Num": 2, "Description": "A Table", "Location": "B4",
                     "Storage Fees": "None", "Paid Last": "None"},
                    {"_id": 3, "shipment num": 3, 'Designer': "Joe", \
                     "Client": "CALEB", "Volume": 100, "Date Entered": datetime(2019, 2, 5), \
                     "Img Num": 3, "Description": "A Table", "Location": "C4",
                     "Storage Fees": "None", "Paid Last": datetime(2019, 8, 10)},
                    {"_id": 4, "shipment num": 4, 'Designer': "Joe", \
                     "Client": "CHARLIE", "Volume": 100, "Date Entered": datetime(2019, 3, 20), \
                     "Img Num": 4, "Description": "A Table", "Location": "D4",
                     "Storage Fees": "None", "Paid Last": datetime.today()}]

        all_inv.insert_many(inv_data)



