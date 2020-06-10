# from flask import Flask
# from flask_pymongo import PyMongo
# from flask_login import LoginManager
# from dotenv import load_dotenv
# import os

# #TODO the url_for argument has to be changed to the blueprintName.functionName
# load_dotenv()

# #TODO before pushing. change urls in js scripts. Remove dotenv. Remove Debug

# ADMIN_PASS = os.environ["ADMIN_PASSWORD"]
# SUPEREMPLOYEE_PASS = os.environ["SUPEREMPLOYEEPASSWORD"]
# USER_PASS = os.environ["USERPASSWORD"]
# EMPLOYEE_PASS = os.environ["EMPLOYEEPASSWORD"]
# PASSWORDSALT = os.environ["PASSWORDSALT"]
# DBUSERNAME = os.environ["DBUSERNAME"]
# DBPASSWORD = os.environ["DBPASSWORD"]
# APPSECRETKEY = os.environ["APPSECRETKEY"]
# MONGODB_URI = os.environ["MONGODB_URI"]

# app = Flask(__name__)
# app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = APPSECRETKEY
# app.config["SECURITY_PASSWORD_SALT"] = PASSWORDSALT
# app.static_folder = 'static'
# #app.config["SECURITY_TOKEN_MAX_AGE"] = True Will set auth token on a timer


# login_manager = LoginManager(app)

# mongo = PyMongo(app, uri="mongodb://"+DBUSERNAME+":"+DBPASSWORD+MONGODB_URI)
# db = mongo.db


# #from auth.auth_routes import auth_bp
# from base.base import base_bp

# #app.register_blueprint(auth_bp)
# app.register_blueprint(base_bp)


from app import create_app

app = create_app()

app.run()