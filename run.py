from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
#TODO update SECRET KEY and SECURITY PASSWORD SALT
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config["MONGO_URI"] = "mongodb://localhost:27017/webdb"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config["SECURITY_PASSWORD_HASH"] = "sha512_crypt"
app.config["SECURITY_PASSWORD_SALT"] = "T"
app.static_folder = 'static'
#app.config["SECURITY_PASSWORD_SINGLE_HASH"] = True
# app.config["SECURITY_TOKEN_MAX_AGE"] = True Will set auth token on a timer

login_manager = LoginManager(app)
mongo = PyMongo(app, uri="mongodb://localhost:27017/webdb")
db = mongo.db
