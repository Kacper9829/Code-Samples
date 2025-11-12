from app import create_app, db 
from flask_migrate import Migrate

app = create_app()
#responsible for data migration and database updates
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)