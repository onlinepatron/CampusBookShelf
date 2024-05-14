from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            print("User authenticated successfully.")  # Debug statement
            return redirect(url_for('main'))  # Redirect to main page after login
        else:
            flash('Invalid username or password')
            print("Authentication failed.")  # Debug statement
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Please fill out all fields.')
            print("Form fields missing")  # Debug print
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            print("Username already exists")  # Debug print
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        print("User registered and logged in")  # Debug print
        return redirect(url_for('main'))
    return render_template('signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
