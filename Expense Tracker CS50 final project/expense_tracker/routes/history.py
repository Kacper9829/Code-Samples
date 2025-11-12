from app import db
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import extract, func, case 
from models import User, Expense, Currency
from datetime import datetime


#create blueprints for history route 
history_bp = Blueprint('history', __name__)

#create history route to display expense date from selected year
@history_bp.route('/history', methods=['GET', 'POST'])
@login_required
def history():

    #set the default currency
    default_currency = db.session.query(Currency).filter(Currency.id == User.user_default_currency_id).first()

    #set selected year based on form submission or default to current year
    selected_year = request.form.get('year')
    if selected_year:
        year = int(selected_year)   
    else:
        year = datetime.now().year

    # get all distinct years that the user has expenses in
    years_query = (
        db.session.query(extract('year', Expense.date).label('year'))
        .filter(Expense.user_id == current_user.id)
        .group_by(extract('year', Expense.date))
        .order_by(extract('year', Expense.date))
        .all()
    )
    # convert to integers in one line
    years = [int(y[0]) for y in years_query]  


    # query to get all the expenses for the selected year and total expenses
    expenses = (db.session.query(Expense)
            .filter(
                extract('year', Expense.date)==year,
                Expense.user_id==current_user.id
        ).all()
    )
    total_expenses = (db.session.query(
        func.sum(
            case(
                (Currency.exchange_rate_to_euro != None,
                 Expense.amount *
                 (default_currency.exchange_rate_to_euro / Currency.exchange_rate_to_euro)),
                else_=Expense.amount
                )
            )
        )   
        .join(Currency, Expense.currency_id == Currency.id)\
        ).filter(
            Expense.user_id == current_user.id,
            extract('year', Expense.date) == selected_year,
        ).scalar() or 0
    
    return render_template('history.html', expenses=expenses, year=year, years=years, total_expenses=total_expenses)