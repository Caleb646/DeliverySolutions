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

    tag_num = fields.IntegerField("Tag Number:", validators=[validators.optional()])

    shipment_num = fields.IntegerField("Shipment Number:", validators=[validators.optional()])

    designer = fields.SelectField("Designer:", choices=[], validators=[validators.optional()])

    client = fields.SelectField("Client:", choices=[], validators=[validators.optional()])

    submit = fields.SubmitField("Submit")
