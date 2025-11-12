from app import db, create_app
from models import Category
from data.categories import default_categories

app = create_app()
# seeds the category table with category data form data/categories.py
with app.app_context():
    for name in default_categories:
        #check if category is already added
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()
    print("Default categories added!")