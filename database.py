from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
from datetime import datetime
from run import db

class User(UserMixin):

    """Creates a User obj to pass to flask_login.
    Also validates a user based on their given roles
    which are: user, admin, super_employee, employee"""

    def __init__(self, username, email, password, roles, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self.roles = roles
        #self._id = uuid.uuid4().hex if _id is None else _id


    @staticmethod
    def check_pass(passwordin_db, passwordto_check):
        return check_password_hash(passwordin_db, passwordto_check)

    @staticmethod
    def check_roles(user: db.Users):

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

        Users.insert_one({"_id": 1, "username" : "Caleb", "password" : generate_password_hash('Anna'),
                          "roles" : [ "admin" ], "email" : "calebthomas646@yahoo.com" })
        Users.insert_one({"_id": 2, "username": "Joe", "password": generate_password_hash('Anna'),
                          "roles": ["user"], "email": "calebthomas646@yahoo.com"})
        Users.insert_one({"_id": 3, "username": "Jill", "password": generate_password_hash('Anna'),
                          "roles": ["super_employee"], "email": "calebthomas646@yahoo.com"})
        Users.insert_one({"_id": 4, "username": "Jane", "password": generate_password_hash('Anna'),
                          "roles": ["employee"], "email": "calebthomas646@yahoo.com"})

        metadata = db["MetaData"]

        meta_list = [{'Name': "Inv Data", "shipment num": 1, "tag num": 1},
                    {'Name': "Designer Info", "Designers": ['JOHN', 'PAUL', 'MARY', 'JONE']},
                     {"Name": "User Ids", "id": 4, "Editable Fields":["email", "username"]}]

        metadata.insert_many(meta_list)



        data_list = [{'Name': "JOHN", "clients": ["BOB", "JANE"]},
                     {'Name': "PAUL", "clients": ["CAT", "JILL"]},
                     {'Name': "MARY", "clients": ["LEVI", "CALEB"]},
                     {'Name': "JONE", "clients": ["MADDIE", "CHARLIE"]}]

        metadata.insert_many(data_list)

        all_inv = db["AllInv"]

        inv_data = [{"_id": 1, "shipment num": 1, 'Designer': "JOHN",\
                    "Client": "BOB", "Volume":100, "Date Entered": datetime.now(),\
                     "Img Num": 1, "Description": "A Table", "Location": "A4", "Storage Fees": "None"},
                    {"_id": 2, "shipment num": 2, 'Designer': "PAUL", \
                     "Client": "JILL", "Volume": 100, "Date Entered": datetime.now(), \
                     "Img Num": 2, "Description": "A Table", "Location": "B4", "Storage Fees": "None"},
                    {"_id": 3, "shipment num": 3, 'Designer': "MARY", \
                     "Client": "CALEB", "Volume": 100, "Date Entered": datetime.now(), \
                     "Img Num": 3, "Description": "A Table", "Location": "C4", "Storage Fees": "None"},
                    {"_id": 4, "shipment num": 4, 'Designer': "JONE", \
                     "Client": "CHARLIE", "Volume": 100, "Date Entered": datetime.now(), \
                     "Img Num": 4, "Description": "A Table", "Location": "D4", "Storage Fees": "None"}]

        all_inv.insert_many(inv_data)



