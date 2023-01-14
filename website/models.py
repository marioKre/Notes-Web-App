from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Creating a class for notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    # Using func to represent and store a timestamp with timezone in a database
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Setting up relationship with Note database
    # One to many relationship, user can have multiple notes
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Creating a class for user, inherits from db.Model and UserMixin which is used for user authentication
# Defining database fields
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Creates a virtual field on the User class which allows accessing the notes of the user
    # Relationship is set up using the user_id foreign key on the Note class.
    notes = db.relationship("Note")
