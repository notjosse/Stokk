from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from stock_api.models import User, Item

# RegisterForm is a class that defines the fields for the Form for creating user accounts
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username not available.')

    def validate_email_address(self, email_to_check):
        user = User.query.filter_by(email_address=email_to_check.data).first()
        if user:
            raise ValidationError('Email already in use.')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()]) # uses the Length validator package from wtform.validators to esure length of username is between 2 and 30 chars
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()]) # uses the EqualTo validator package from wtform.validators to ensure passwrod2 matches password1
    submit = SubmitField(label='Register')

# LoginForm is the class for the form displayed on the lgoin page to validate login information
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')


class CreateItemForm(FlaskForm):
    def validate_item_exists(self, item_to_check):
        item = Item.query.filter_by(name=item_to_check.data).first()
        if item:
            raise ValidationError('Item already exists.')

    def validate_barcode(self, barcode_to_check):
        barcode = Item.query.filter_by(barcode=barcode_to_check.data).first()
        if barcode:
            raise ValidationError('Barcode already in use.')

    name = StringField(label='Item Name:', validators=[Length(min=2, max=30), DataRequired()]) # uses the Length validator package from wtform.validators to esure length of username is between 2 and 30 chars
    barcode = StringField(label='12-Digit Barcode:', validators=[Length(min=12, max=12), DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[Length(min=1, max=1024), DataRequired()]) # uses the EqualTo validator package from wtform.validators to ensure passwrod2 matches password1
    submit = SubmitField(label='Add Item')
