from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate

    @app.route("/")
    def home():
        return "Welcome to CrisisDefuse!"

    return app

if __name__ == "__main__":
    app = create_app()

    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     print("Database created!")

    app.run(debug=True)
