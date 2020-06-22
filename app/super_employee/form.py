from wtforms import validators, form, fields, SelectMultipleField, widgets, Form
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm



class SearchForm(FlaskForm):#validators=[validators.optional()] 

    tag_num = fields.IntegerField("Tag Number:", validators=[validators.optional()] )

    shipment_num = fields.IntegerField("Shipment Number:", validators=[validators.optional()] )

    designer = fields.SelectField("Designer:", choices=[], validators=[validators.optional()] )

    client = fields.SelectField("Client:", choices=[], validators=[validators.optional()] )

    submit = fields.SubmitField("Submit")

    def validate(self):##stops flask form from flagging dynamically added items
        return True


class MultiCheckboxField(SelectMultipleField):

    widget = widgets.ListWidget(prefix_label=False)

    option_widgets = widgets.CheckboxInput()


class EditForm(FlaskForm):

    choices = MultiCheckboxField('Routes')

    designer = fields.SelectField("Move to Designers Inventory:", choices=[], validators=[validators.optional(), validators.NoneOf((None, "EMPTY"))])
    
    client = fields.SelectField("Pick Client too:", choices=[], validators=[validators.optional(), validators.NoneOf((None, "EMPTY"))])

    delete = fields.SubmitField("Delete Checked Items")

    move = fields.SubmitField("Move to Chosen Inventory")

class StorageFees(FlaskForm):

    designer = fields.SelectField("Designer:", choices=[], validators=[validators.required()])

    client = fields.SelectField("Client:", choices=[], validators=[validators.optional()])

    submit = fields.SubmitField()


class AddForm(FlaskForm):

    designer = fields.SelectField("Designer:", choices=[], validators=[validators.optional()])

    client = fields.SelectField("Client:", choices=[], validators=[validators.optional()])

    volume = fields.IntegerField("Volume:", validators=[validators.optional()])

    description = fields.StringField("Description:", validators=[validators.optional()])

    location = fields.StringField("Location:", validators=[validators.optional()])

    image_num = fields.IntegerField("Image number:", validators=[validators.optional()])

    submit = fields.SubmitField("Submit")