from app import db
from flask import flash, redirect, render_template, request, Blueprint, abort
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Currency
from helpers import update_currency_rates

# create settings blueprint
settings_bp = Blueprint('settings', __name__)

# set up settings page
@settings_bp.route('/settings')
@login_required
def settings_page():
    currencies = Currency.query.all()
    return render_template('settings.html', currencies=currencies)

#set up update rates route to update currencies rates, only for admin
@settings_bp.route('/update_rates', methods =["POST"])
@login_required
def update_rates():
    #check if user is and admin
    if not current_user.is_admin:
        abort(403)
    #update currencies using helpers function 
    update_currency_rates()
    flash("Exchange rates updated successfully!", "success")
    return redirect('/settings')

# set up a route to change username 
@settings_bp.route('/change_username', methods = ["POST"])
@login_required
def change_username():
    # get new username and search for it in database to 
    new_username = request.form.get('username')
    find_user = User.query.filter(User.username==new_username).first()
    # check if it's taken
    if find_user:
        flash("Username already taken!", "danger")
        return redirect('/settings')
    if not new_username:
        flash("Enter new username!", "danger")
        return redirect('/settings')

    # serach for user to change their username
    user = User.query.filter(User.id == current_user.id).first()
    # change the username
    user.username = new_username
    db.session.commit()

    flash("Username updated successfully!", "success")
    return redirect('/settings')

# set up a route change password 
@settings_bp.route('/change_password', methods = ["POST"])
@login_required
def change_password():

    #get the new and current password
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    user = User.query.filter(User.id==current_user.id).first()

    # check if passwords are entered
    if not current_password or not new_password:
        flash("Current password and new password fields can't be empty!", "danger")
        return redirect('/settings')
    # check if current passwords is entered
    if not check_password_hash(user.password_hash, current_password):
        flash("Current password incorrect!", "danger")
        return redirect('/settings')
    # check if passwords are different
    if check_password_hash(user.password_hash, new_password):
        flash("New password can't be the same as the current one!", "danger")
        return redirect('/settings')
    
    #hash the new password and update it in the database 
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    flash("Password updated successfully!", "success")
    return redirect('/settings')

# set up a route to delete the account of current user
@settings_bp.route('/delete_account', methods = ["POST"])
@login_required
def delete_account():
    #querry the current user
    user = User.query.filter(User.id==current_user.id).first()
    # delete the current user using cascade deletion
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} and all their data have been deleted.', 'success')
    return redirect('/register')

# change users default currency
@settings_bp.route('/change_default_currency', methods = ["POST"])
@login_required
def change_default_currency():
    #get the new currency
    new_default_currency = request.form.get('default_currency')

    # update users default currency
    user = User.query.filter(User.id == current_user.id).first()
    user.user_default_currency_id = new_default_currency
    db.session.commit()
    flash("Default Currency Updated", "success")
    return redirect('/settings')
    