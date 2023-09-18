from flask import Flask

from .extensions import db, login_manager, bcrypt
from .routes import main

def create_app(database_uri="sqlite:///stock_api.db"):
    # App Configs
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SECRET_KEY'] = '11adb4aa687ca51822ad4b14' # TODO: MUST MAKE THIS AN ENV VARIABLE

    # SQLAlchemy Configs
    db.init_app(app) # initializes the database using the uri provided at 'app.config['SQLALCHEMY_DATABASE_URI']'

    # Bcrypt Configs
    bcrypt.init_app(app)

    # Login Manager Configs
    login_manager.init_app(app)
    login_manager.login_view = "main.login" # name of the route to our login page
    login_manager.login_message_category = "info" # category for our flash message
    login_manager.login_message = "Please login or register an account." # flash message contents  

    # Routes Blueprint
    app.register_blueprint(main)

    return app