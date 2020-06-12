from werkzeug.security import check_password_hash
from wtforms import validators, form, fields, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

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

    movetto_field = fields.SelectField("Move to Designers Inventory:", choices=[], validators=[validators.optional()])
    
    client = fields.SelectField("Pick Client too:", choices=[], validators=[validators.optional()])

    delete = fields.SubmitField("Delete Checked Items")

    move = fields.SubmitField("Move to Chosen Inventory")

class UserEditForm(FlaskForm):

    choices = MultiCheckboxField('Routes', coerce=int)

    roles = fields.SelectField("Roles:", choices=[("admin", "admin"),
                                                  ("user", "user"),
                                                  ("super_employee", "super_employee"),
                                                  ("employee", "employee")], validators=[validators.optional()])

    editable_fields = fields.SelectField("Choose One Field to Change:", validators=[validators.optional()])

    change_to = fields.StringField("Change Chosen Field To", validators=[validators.optional()])

    add_client = fields.StringField("Change Field To", validators=[validators.optional()])


class UserPasswordForm(FlaskForm):

    admin_password = fields.PasswordField("Current Admin Password", validators=[validators.required()])

    new_user_password = fields.StringField("New User Password", validators=[validators.required()])


class CreateWorker(FlaskForm):

    username = fields.StringField("Enter Username", validators=[validators.required()])

    password = fields.PasswordField("Enter Password", validators=[validators.required()])

    email = EmailField("Enter Email", validators=[validators.required()])

    roles = fields.SelectField("Enter User Role:", choices=[("admin", "admin"),
                                                  ("super_employee", "super_employee"),
                                                  ("employee", "employee")], validators=[validators.required()])
    submit = fields.SubmitField()


class CreateUser(FlaskForm):

    username = fields.StringField("Enter Username", validators=[validators.required()])

    password = fields.PasswordField("Enter Password", validators=[validators.required()])

    email = EmailField("Enter Email", validators=[validators.required()])

    known_clients = fields.StringField("Enter Known Clients", validators=[validators.optional()])

    submit = fields.SubmitField()


class StorageFees(FlaskForm):

    designers = fields.SelectField("Designer:", choices=[], validators=[validators.required()])

    clients = fields.SelectField("Clients:", choices=[], validators=[validators.optional()])

    submit = fields.SubmitField()