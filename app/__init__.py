from dotenv import load_dotenv
from flask import Flask, current_app
from flask_login import LoginManager
from flask_pymongo import PyMongo
import os


#TODO the url_for argument has to be changed to the blueprintName.functionName
load_dotenv()

#TODO before pushing. change urls in js scripts. Remove dotenv. Remove Debug

ADMIN_PASS = os.environ["ADMIN_PASSWORD"]
SUPEREMPLOYEE_PASS = os.environ["SUPEREMPLOYEEPASSWORD"]
USER_PASS = os.environ["USERPASSWORD"]
EMPLOYEE_PASS = os.environ["EMPLOYEEPASSWORD"]
PASSWORDSALT = os.environ["PASSWORDSALT"]
DBUSERNAME = os.environ["DBUSERNAME"]
DBPASSWORD = os.environ["DBPASSWORD"]
APPSECRETKEY = os.environ["APPSECRETKEY"]
MONGODB_URI = os.environ["MONGODB_URI"]


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = APPSECRETKEY
app.config["SECURITY_PASSWORD_SALT"] = PASSWORDSALT
app.static_folder = 'static'
#app.config["SECURITY_TOKEN_MAX_AGE"] = True Will set auth token on a timer


login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.login_message = ('Please log in.')
login_manager.init_app(app)


mongo = PyMongo(app, uri="mongodb://"+DBUSERNAME+":"+DBPASSWORD+MONGODB_URI)
db = mongo.db



try:

    #can set url prefix by url_prefix="/auth"
    from app.auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.base.base_routes import base_bp
    app.register_blueprint(base_bp)

    from app.admin.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app import database, forms, global_util

except (ImportError, ImportWarning) as e:
    print("Package Name: {} File Name: {} ERROR: {}".format(__name__, __file__, e))          





