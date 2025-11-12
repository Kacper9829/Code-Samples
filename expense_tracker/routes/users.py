from app import db
from datetime import datetime, timedelta
from flask import flash, redirect, render_template, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from models import User, Expense, Currency
from werkzeug.security import check_password_hash, generate_password_hash

# create a flask blueprint for users route
users_bp = Blueprint('users', __name__)

# main site/index.html data set up for latests expenses (90days)
@users_bp.route('/')
def dashboard():
    if current_user.is_authenticated:
        name = current_user.first_name
        ninety_days_ago = (datetime.now() - timedelta(days = 90)).date()
        expenses = Expense.query.filter(Expense.date>=ninety_days_ago, Expense.user_id==current_user.id).all()

        return render_template('index.html', name=name, expenses=expenses)
    else:
        return redirect('/login')
    
#loign route using flask login manger   
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    # get users login (email or username) and password
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')

        #check if user entered correct login
        user = User.query.filter(
            or_(User.username == login, User.email == login)
        ).first()

        #check if user entered correct password
        if (user and check_password_hash(user.password_hash, password)):
            #log in using login manger
            login_user(user)
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid username/email or password!', 'danger')
            return redirect('/login')
    return render_template('login.html')

# route that logs user out
@users_bp.route('/logout')
@login_required
def logout():
    #log out using login manger
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect('/login')

# route to register a user
@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    #query currencies for select menu
    currencies = Currency.query.all()
    if request.method == "POST":
        #get data from the user to add into the database
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        username = request.form.get('username')
        default_currency = request.form.get('default_currency')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm')

        #check if all fields are filled correctly
        if not (first_name or email or username or password or confirm_password):
            flash('Please fill out all fields!', 'danger')
            return redirect('/register')
        #check if password is the same as confirmation 
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect('/register')
        #check if username is taken
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect('/register')

        # create new user object and add to the database
        new_user = User(
            first_name=first_name,
            email=email,
            username=username,
            user_default_currency_id=default_currency,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect('/login')
    return render_template('register.html', currencies=currencies)
