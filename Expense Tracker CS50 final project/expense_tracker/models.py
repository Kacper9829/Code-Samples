from app import db
from flask_login import UserMixin

#create User table 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    user_default_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=True)
    user_default_currency = db.relationship('Currency', backref='users', lazy='joined')
    is_admin = db.Column(db.Boolean, default=False)  

#create Expense table 
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref='expenses', lazy='joined')
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=True)
    currency = db.relationship('Currency', backref='expenses', lazy='joined')
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=True)

#create Category table 
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    
#create Currency table     
class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    exchange_rate_to_euro = db.Column(db.Float, nullable=True) 