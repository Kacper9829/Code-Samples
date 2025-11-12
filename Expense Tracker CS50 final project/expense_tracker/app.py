from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# sets flasks login manager, SQL Alchemy database and migration
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


#flask login manager route
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# main app creating function
def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey123"
    app.config.from_object('config.Config')
    
    # initialize database and migration
    db.init_app(app)
    migrate.init_app(app, db)

    #initialize flask login manger
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    # import database models and route blueprints 
    from models import User, Expense, Category, Currency
    from routes.settings import settings_bp
    from routes.users import users_bp
    from routes.expenses import expenses_bp
    from routes.stats import stats_bp
    from routes.history import history_bp
    
    # register blueprints of routes
    app.register_blueprint(settings_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(history_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run

