from flask import Blueprint, render_template, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, current_user
from stock_api.forms import RegisterForm, LoginForm
from stock_api.models import User
from stock_api import db



authentication_bp = Blueprint("authentication", __name__, template_folder="templates")


@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('historical_data.home'))

    form = LoginForm()

    if form.validate_on_submit():
        # first checks if the user exists in the database
        attempted_user = User.query.filter_by(username=form.username.data).first()
        # Then checks if the password provided matches the hashed password in the database
        if attempted_user and attempted_user.check_password(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success, you are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('historical_data.home'))
        else:
            flash('Incorrect username or password.', category='danger')


    return render_template('login.html', form=form)


# Route that handles requests and renders the template for the Register Page; handles get and post requests
@authentication_bp.route('/register', methods=['GET', 'POST'])
def register(): 

    if current_user.is_authenticated:
        return redirect(url_for('historical_data.home'))

    form = RegisterForm()

    # Verify the fields from the FORM and make sure the user has clicked on the 'submit' button
    if form.validate_on_submit():
        
        user_to_create = User(username=form.username.data, 
                              email_address=form.email_address.data,
                              password=form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully, you are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('historical_data.home'))


    if form.errors != {}: # if there are errors from the validations
        for error_msg in form.errors.values():
            flash(f'Error: {error_msg[0]}', category='danger')

    return render_template('register.html', form=form)


@authentication_bp.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.', category='info')
    return redirect(url_for('authentication.login'))