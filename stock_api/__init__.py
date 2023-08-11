from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import json

# Nasdaq api key
try:
    api_key = json.load(open('./api_key.json', 'r'))["key"]
except:
    api_key = "no_key"


# App Configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_api.db'
app.config['SECRET_KEY'] = '11adb4aa687ca51822ad4b14' # TODO: MUST MAKE THIS AN ENV VARIABLE

# SQLAlchemy Configs
db = SQLAlchemy(app) # initializes the database using the uri provided at 'app.config['SQLALCHEMY_DATABASE_URI']'

# Bcrypt Configs
bcrypt = Bcrypt(app)

# Login Manager Configs
login_manager = LoginManager(app)
login_manager.login_view = "login" # name of the route to our login page
login_manager.login_message_category = "info" # category for our flash message
login_manager.login_message = "Please login or register an account." # flash message contents

# Necessary imports
from stock_api import routes