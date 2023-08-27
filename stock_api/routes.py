from stock_api import app, api_key
from flask import render_template, redirect, url_for, flash, request, send_file
from stock_api.models import User
from stock_api.forms import RegisterForm, LoginForm
from stock_api import db
from flask_login import login_user, logout_user, login_required, current_user
import requests, json

# Route to redirect '/home/' --> '/'  
@app.route("/home/", methods=['GET', 'POST'])
def home_home():
    return redirect(url_for('home'))

# routes to the home page if route is: '/'
@app.route("/", methods=['GET', 'POST'])
@login_required
def home():

    data = None
    start_date, end_date = None, None

    if request.method == "GET":
        # Historical Data Request
    
        ticker = request.args.get('stock-query')
        start_date = request.args.get('start-date')
        end_date = request.args.get('end-date')

        if ticker and len(ticker) <= 4 and current_user.get_budget() >= 50:
            # reduce the budget by 50 coins 
            current_user.reduce_budget()
            
            # make the request to the nasdaq api
            r = requests.get(f'https://data.nasdaq.com/api/v3/datatables/WIKI/PRICES?date.gte={start_date}&date.lte={end_date}&ticker={ticker}&qopts.columns=date,ticker,open,high,low,close,volume&api_key={api_key}')
            data = r.json()["datatable"]["data"]
            if r.json()["datatable"]["data"] == []:
                data = None

        return render_template('home.html', data=data)


    if request.method == "POST":
    # Download JSON Data:
        export_data = request.form.get('export-json')
        if export_data:
            with open('./stock_api/staging/data.json', 'w', encoding='UTF8') as f:
                json.dump(export_data, f)
                
            return send_file('./staging/data.json', as_attachment=True)

        return redirect(url_for('home'))


# Route that handles requests and renders the template for the Register Page; handles get and post requests
@app.route('/register', methods=['GET', 'POST'])
def register(): 
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

        return redirect(url_for('home'))


    if form.errors != {}: # if there are errors from the validations
        for error_msg in form.errors.values():
            flash(f'Error: {error_msg[0]}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password.', category='danger')


    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.', category='info')
    return redirect(url_for('login'))