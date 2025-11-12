from app import db
import calendar
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import extract, func, case
from models import User, Expense, Category, Currency
from helpers import monthly_avg
from datetime import datetime

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    # assign default values first
    total_expenses = 0
    total_per_cat = []
    monthly_expenses = 0
    highest_expense = None
    avg_daily = 0  
    default_currency = db.session.query(Currency).filter(Currency.id == User.user_default_currency_id).first()

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
    
    # set selected year and month based on form submission or defaults
    if request.method == 'POST':
        selected_year = int(request.form.get('year', years[-1] if years else datetime.now().year))
        selected_month = int(request.form.get('month', datetime.now().month))
    else:
        selected_year = years[-1] if years else datetime.now().year
        selected_month = datetime.now().month
    
    
    # query to get total expenses per year with converted values if amount is in different currency than the default
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
        .filter(
            Expense.user_id == current_user.id,
            extract('year', Expense.date) == selected_year,
        ).scalar()
    )

    # query to get total expenses per category with converted values if amount is in different currency than the default
    total_per_cat = (db.session.query(
        Category.name,
        func.sum(
            case(
                (Currency.exchange_rate_to_euro != None,
                Expense.amount *
                (default_currency.exchange_rate_to_euro / Currency.exchange_rate_to_euro)),
                else_=Expense.amount
                )).label('converted_total')  
        )
        ).join(Expense, Expense.category_id == Category.id)\
         .join(Currency, Expense.currency_id == Currency.id)\
         .filter(Expense.user_id == current_user.id)\
         .group_by(Category.name).all()
    
    # query the highest expense using the converted amount with converted values if amount is in different currency than the default
    converted_amount = case(
        (
        (Currency.exchange_rate_to_euro != None),
        Expense.amount * (default_currency.exchange_rate_to_euro / Currency.exchange_rate_to_euro)
        ),
        else_=Expense.amount
    ).label('converted_amount')

    
    highest_expense = (
        db.session.query(Expense, converted_amount)
        .join(Currency, Expense.currency_id == Currency.id)
        .join(Category, Expense.category_id == Category.id)
        .filter(Expense.user_id == current_user.id)
        .order_by(converted_amount.desc())  
        .first()
        )   
    
    # query to get average daily expense with converted values if amount is in different currency than the default
    daily_totals = (db.session.query(
        func.date(Expense.date).label('date'),
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
            .filter(Expense.user_id == current_user.id)\
            .group_by(func.date(Expense.date))\
            .subquery()
            )
                  
    avg_daily = db.session.query(func.avg(daily_totals.c.sum)).scalar()

    # use helpers monthly average function to calculate 
    avg_per_month = monthly_avg(selected_year)

    monthly_stats = []

    #get current year
    current_year = datetime.now().year
    # query to get total expenses for the selected year
    total_expenses_selected_year = (db.session.query(
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
        .filter(
            Expense.user_id == current_user.id,
            extract('year', Expense.date) == current_year,
        ).scalar()
        )
    # query to get total expenses for the previous year to the selected one
    total_expenses_previous_year = (db.session.query(
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
        .filter(
            Expense.user_id == current_user.id,
            extract('year', Expense.date) == current_year - 1,
        ).scalar()
        )
    
    # calculate difference
    if total_expenses_previous_year and total_expenses_selected_year:
        percent_change = ((total_expenses_selected_year - total_expenses_previous_year) / total_expenses_previous_year) * 100
    else:
        percent_change = 0
    # format percent change for display
    percent_change_display = f"{percent_change:.2f}%" if percent_change is not None else "N/A"


    # query and fill in monthly stats
    for month in range(1, 13):
        # query the monthly total with converted values if amount is in different currency than the default
        monthly_total = (
            db.session.query(
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
            .filter(
                Expense.user_id == current_user.id,
                extract('year', Expense.date) == selected_year,
                extract('month', Expense.date) == month
            ).scalar() or 0
        )
        # query the most popular category  
        top_monthly_category = (
            db.session.query(
                Category.name,
                func.sum(Expense.amount).label('total')
            )
            .join(Category, Category.id == Expense.category_id)
            .filter(
                Expense.user_id == current_user.id,
                extract('year', Expense.date) == selected_year,
                extract('month', Expense.date) == month
            )
            .group_by(Category.name)
            .order_by(func.sum(Expense.amount).desc())
            .first()
            )
        # query the monthly highest expense with converted values if amount is in different currency than the default
        monthly_highest_expense = (
            db.session.query(
            case(
                (Currency.exchange_rate_to_euro != None,
                 Expense.amount *
                 (default_currency.exchange_rate_to_euro / Currency.exchange_rate_to_euro)),
                else_=Expense.amount
                )
            )   
            .join(Currency, Expense.currency_id == Currency.id)
            .filter(
                Expense.user_id == current_user.id,
                extract('year', Expense.date) == selected_year,
                extract('month', Expense.date) == month
            )
            .order_by(Expense.amount.desc())
            .first()
        )
        highest_amount_per_month = monthly_highest_expense[0] if monthly_highest_expense else 0
        
        # append monthly statistics
        monthly_stats.append({
            'month': calendar.month_name[month], 
            'total': monthly_total,
            'highest': highest_amount_per_month,
            'top_category': top_monthly_category
        })
    
    # render the stats template with the queried data
    return render_template(
        'stats.html',
        total_expenses=total_expenses,
        total_per_cat=total_per_cat,
        monthly_expenses=monthly_expenses,
        highest_expense=highest_expense,
        avg_daily_expense=avg_daily,
        years=years,
        avg_per_month=avg_per_month,
        monthly_stats=monthly_stats,
        selected_year=selected_year,
        percent_change_display=percent_change_display,
        default_currency=default_currency
    )

