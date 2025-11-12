from sqlalchemy import extract, func
from app import db
import requests
from models import Expense, Currency
from flask_login import current_user

# helper function that gets monthly average in selected year
def monthly_avg(year):
    total = db.session.query(
        extract('month', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).filter(
        Expense.user_id==current_user.id,
        extract('year', Expense.date) == int(year)
    ).group_by(extract('month', Expense.date)).subquery()

    return db.session.query(func.avg(total.c.total)).scalar() or 0

# helper function that updates currency exchange rate to Euro to the Currency table using API from "https://www.exchangerate-api.com"
def update_currency_rates(base="EUR"):
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("result") != "success":
            print("Failed to fetch exchange rates")
            return
        
        rates = data["rates"]
        for currency in Currency.query.all():
            if currency.code in rates:
                currency.exchange_rate_to_euro = rates[currency.code]
                print(f"{currency.code} -> {rates[currency.code]}")
        
        db.session.commit()
        print("Rates updated successfully!")
    except Exception as e:
        print(f"Currency update error: {e}")