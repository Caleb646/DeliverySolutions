from werkzeug.security import check_password_hash
from wtforms import validators, form, fields, SelectMultipleField, widgets
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


class MultiCheckboxField(SelectMultipleField):

    widget = widgets.ListWidget(prefix_label=False)

    option_widgets = widgets.CheckboxInput()


class EditForm(FlaskForm):

    choices = MultiCheckboxField('Routes', coerce=int)

    movetto_field = fields.SelectField("Move to Designers Inv:", choices=[], validators=[validators.optional()])
    
    client = fields.SelectField("Pick Client too:", choices=[], validators=[validators.optional()])


class UserEditForm(FlaskForm):

    choices = MultiCheckboxField('Routes', coerce=int)

    roles = fields.SelectField("Roles:", choices=["admin", "user", "super_employee", "employee"], validators=[validators.optional()])
    
    #client = fields.SelectField("Pick Client too:", choices=[], validators=[validators.optional()])


