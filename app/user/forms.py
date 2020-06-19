from werkzeug.security import check_password_hash
from wtforms import validators, form, fields, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from app.constants import sort_methods

#Sort Methods
SPECIFIC_CLIENT_SUM = sort_methods[0]
ALL_CLIENTS_SUM = sort_methods[1]
INDIVIDUAL_ITEMS = sort_methods[2]


class UserSearch(FlaskForm):

    tag_num = fields.IntegerField("Tag Number:", validators=[validators.optional()])

    shipment_num = fields.IntegerField("Shipment Number:", validators=[validators.optional()])

    client = fields.SelectField("Client:", choices=[], validators=[validators.optional()])

    submit = fields.SubmitField("Submit")


class StorageFeesSearch(FlaskForm):

    sort_methods = fields.SelectField("Sorting Methods:",\
                            choices=[(SPECIFIC_CLIENT_SUM, "Specific Client Fees Sum"),\
                                (ALL_CLIENTS_SUM, "All Clients Fees Summed"),\
                                (INDIVIDUAL_ITEMS, "Items Summed Individually")],\
                                validators=[validators.optional()])

    clients = fields.SelectField("")

    submit = fields.SubmitField("Submit")