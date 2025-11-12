from app import db, create_app
from models import Currency
from data.currency import common_currencies

# seeds the currency table with currency data form data/currency.py
app = create_app()
with app.app_context():
    for code, name in common_currencies.items():
        # check if currency is already added
        if not Currency.query.filter_by(name=name).first():
            db.session.add(Currency(name=name, code=code))
    db.session.commit()
    print("Currencies added!")
    