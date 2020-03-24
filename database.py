from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
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
    pass
    #Users = db["Users"]
    #Users.insert_one({"username" : "Caleb", "password" : generate_password_hash('Anna'),
                      #"roles" : [ "admin" ], "email" : "calebthomas646@yahoo.com" })
#     MetaData = db["MetaData"]
#
#     data_list = [{'Name': "JOHN", "clients": ["BOB", "JANE"]},
#      {'Name': "PAUL", "clients": ["CAT", "JILL"]},
#      {'Name': "MARY", "clients": ["LEVI", "CALEB"]},
#      {'Name': "JONE", "clients": ["MADDIE", "CHARLIE"]},
#                  {'Name':"Inv Data", "shipment num": 1, "tag num": 1},
# {'Name':"Designer Info", "Designers":['JOHN', 'PAUL', 'MARY', 'JONE']}]
#
#     admin_input = input("Type y or n if data should be reentered")

    # if admin_input == "y":
    #
    #     for i in range(len(data_list)):
    #         MetaData.insert_one(data_list[i])

 #    all_inv = db["All Inv"]
#  #    john = db["JOHN"]
#  #    paul = db["PAUL"]
#  #    jone = db["JONE"]
#  #    mary = db["MARY"]
#  #
  # info = {'_id': 3, "shipment_num": 3, "Designer": "MARY", "Client": "CHARLIE",
 #"Volume": 100, "Date Entered": Date() , "Img Num": 3, "Description":"A Table"})



