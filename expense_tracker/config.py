import os 

# SQLALCHEMY configuration
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://kac:9829@localhost/expense_tracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")