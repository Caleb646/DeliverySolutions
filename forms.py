from werkzeug.security import check_password_hash
from wtforms import validators, form, fields
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from run import db, app
from database import User


class LoginForm(FlaskForm):

    login = fields.StringField(validators=[validators.required()])

    password = fields.PasswordField(validators=[validators.required()])


class SearchForm(FlaskForm):

    tag_num = fields.IntegerField(validators=[validators.required()])

    designer = fields.SelectField("Designer Name", choices=[])

    client = fields.SelectField("Client Name", choices=[])

