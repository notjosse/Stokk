from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import json

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
# Nasdaq api key
try:
    api_key = json.load(open('./api_key.json', 'r'))["key"]
except:
    api_key = "no_key"
