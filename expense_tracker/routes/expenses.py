from app import db
from flask import flash, redirect, render_template, request, Blueprint
from flask_login import login_required, current_user
from models import User, Expense, Category, Currency

#create expenses route blueprint
expenses_bp = Blueprint('expenses', __name__)

# add new expenses route
@expenses_bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    # query categories and currency for select menu
    categories = Category.query.all()
    currencies = Currency.query.all()
    
    if request.method == 'POST':
        # get user's input 
        amount = request.form.get('amount')
        currency_id = request.form.get('currency')
        category_id = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')

        # check if all the field are filled correctly
        if not amount or not category_id or not date:
            flash('Please fill out all required fields.', 'danger')
            return render_template('add_expense.html', categories=categories)
        # if currency is not selected, use user's default currency
        if currency_id is None:
            currency_id = User.query.filter_by(id=current_user.id).first().user_default_currency_id

        # create expense object and add to the database
        expense = Expense(
            amount=amount,
            currency_id=currency_id,
            category_id=int(category_id),
            date=date,
            description=description,
            user_id=current_user.id
        )
        
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect('/')
    else:
        return render_template('add_expense.html', categories=categories, currencies=currencies)
    
@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expanse(expense_id):
    #search the expense to delete
    expense = Expense.query.filter_by(id = expense_id, user_id = current_user.id).first()
    # check id the expense belongs to the user
    if expense.user_id != current_user.id:
        flash('You are not authorized to delete this expense.', 'danger')
        return redirect('/')
    # delete the expense
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect('/')

@expenses_bp.route('/edit/<int:expense_id>', methods=['POST', 'GET'])
@login_required
def edit_expense(expense_id):
    # query the expense to edit
    expense_to_edit = Expense.query.filter_by(id=expense_id, user_id = current_user.id).first()
    #query categories and currencies for select   
    currencies = Currency.query.all()
    categories = Category.query.all()
    # update the new information of the expense
    if request.method == "POST":
        expense_to_edit.amount = request.form.get('amount')
        expense_to_edit.currency_id = request.form.get('currency')
        expense_to_edit.category_id = int(request.form.get('category'))
        expense_to_edit.date = request.form.get('date')
        expense_to_edit.description = request.form.get('description')
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect('/')
    else:
        return render_template('edit.html', expense=expense_to_edit, categories=categories, currencies=currencies)