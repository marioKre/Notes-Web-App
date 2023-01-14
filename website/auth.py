from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# Initialize blueprint
auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieving data from form
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            # With werkzeug.security, check password hashes
            # Compares hash from form with hash stored in a database
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category='success')
                # With flask_login, set that user is logged in
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            elif not password:
                flash('Please type in your pasword!', category='error')
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash("Account doesn't exist, please sign up", category='error')
            
    return render_template("login.html", user=current_user)

@auth.route("/logout")
# With flask login, make sure route is only accessible when user is logged in
@login_required
def logout():
    # Logout user with flask_login
    logout_user()
    # Redirect to login page, passing in name of a blueprint and function
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods = ['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        # Retrieving data from form
        email = request.form['email']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        # Isolating email to check later if it exists
        user = User.query.filter_by(email=email).first()
        # Stating conditions needed to make a new account
        if user:
            flash('Email already in use', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters!', category='error')
        elif len(first_name) < 2:
            flash('First name should be greater than 1 characters!', category='error')
        elif password1 != password2:
            flash('Passwords not matching', category='error')
        elif len(password1) < 7:
            flash('Password should be at least 7 characters long', category='error')
        else:
            # If all conditions are met, hash password with werkzeug.security, add user to a database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # With flask_login, set that user is logged in
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            # Passing in name of a blueprint and name of a function
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
