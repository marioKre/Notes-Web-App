# The __init__.py file lets the Python interpreter know that a directory contains code for a Python module.
# Enables importing modules from another folder into the project.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Creting SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    # Create an instance of the Flask class
    app = Flask(__name__)
    # Configuring secret key, in production should be hidden
    app.config['SECRET_KEY'] = 'app_secret_key'
    # Setting the URI for the database
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # Initializing SQLAlchemy object and associating it with Flask application
    db.init_app(app)

    # Importing blueprints
    from .views import views
    from .auth import auth

    # Registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Importing database models
    from .models import User, Note

    # Checking if database already exists. If it doesn't, it creates it
    if not path.exists('instance/database.db'):
        with app.app_context():
            db.create_all()

    # Initialize LoginManager and connect it with app
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Providing user_loader callback
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
