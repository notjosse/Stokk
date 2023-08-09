from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

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
