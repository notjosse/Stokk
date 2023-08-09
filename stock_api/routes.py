from stock_api import app, api_key
from flask import render_template, redirect, url_for, flash, request
from stock_api.models import Item, User
from stock_api.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, CreateItemForm
from stock_api import db
from flask_login import login_user, logout_user, login_required, current_user
import requests

# routes to the home page if route is: / or /home
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():

    data = None

    if request.method == "POST":
        ticker = request.form.get('stock-query')

        if ticker and len(ticker) <= 4:
            r = requests.get(f'https://data.nasdaq.com/api/v3/datatables/WIKI/PRICES?date.gte=1997-02-01&date.lte=2017-01-01&ticker={ticker}&qopts.columns=date,ticker,open,high,low,close,volume&api_key={api_key["key"]}')
            data = r.json()["datatable"]["data"]
            if r.json()["datatable"]["data"] == []:
                data = None

    return render_template('home.html', data=data)

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market():

    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    create_item_form = CreateItemForm()
    
    if request.method == "POST":
        # Purchase Item Logic:
        purchased_item_name = request.form.get('purchased-item')
        purchased_item_obj = Item.query.filter_by(name=purchased_item_name).first()
        if purchased_item_obj:
            if current_user.can_purchase(purchased_item_obj):
                purchased_item_obj.buy(current_user)
                flash(f'You purchased {purchased_item_obj.name} for ${purchased_item_obj.price}', category='success')
            else:
                flash(f'Cannot purchase {purchased_item_obj.name}: not enough funds or {purchased_item_obj.name} is already owned.', category='danger')
        

        # Sell Item Logic
        sold_item_name =  request.form.get('sold-item')
        sold_item_obj = Item.query.filter_by(name=sold_item_name).first()
        if sold_item_obj:
            if current_user.can_sell(sold_item_obj):
                sold_item_obj.sell(current_user)
                flash(f'You sold {sold_item_obj.name} for ${sold_item_obj.price}', category='success')
            else:
                flash(f'Cannot sell {sold_item_obj.name}; you do not own this item.', category='danger')
        
        # Add Item Logic:
        if create_item_form.validate_on_submit():
            print("create item form works")
            item_to_create = Item(name=create_item_form.name.data, 
                              barcode=create_item_form.barcode.data,
                              price=create_item_form.price.data,
                              description=create_item_form.description.data)
        
            db.session.add(item_to_create)
            db.session.commit()
            flash(f'Item {item_to_create.name} added to market.', category='success')

        return redirect(url_for('market'))
        
    if request.method == "GET":
        items = Item.query.all() # returns all of the objects stored in the Items table in our sqlite db
        users = User.query.all() # returns all of the objects stored in the Users table in our sqlite db
        # sends the entire list of items above to the template
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, users=users, purchase_form=purchase_form, sell_form=sell_form, owned_items=owned_items, create_item_form=create_item_form)

# this is a dynamic route that renders uses the input of <username> when rendering the page
@app.route("/about")
@app.route("/about/<username>")
def about(username=""):
    return f'<h1>This is the about page for {username}</h1>'


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

        return redirect(url_for('market'))


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
            return redirect(url_for('market'))
        else:
            flash('Incorrect username or password.', category='danger')


    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.', category='info')
    return redirect(url_for('home'))