from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from routes.users import users_bp
from routes.scriptures import scriptures_bp
from routes.blogs import blogs_bp
from routes.errors import errors_bp
from routes.home import home_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate
    
    # ✅ Allow all origins, methods, and headers
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

    # Initialize the JWTManager
    jwt = JWTManager(app)
    
    # Register Blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(scriptures_bp, url_prefix='/scriptures')
    app.register_blueprint(blogs_bp, url_prefix='/blogs')
    app.register_blueprint(errors_bp)  # ✅ No prefix for error handlers
    app.register_blueprint(home_bp)    # ✅ No prefix for the home route

    return app
       

if __name__ == "__main__":
    app = create_app()
    
    # Create the database and tables
    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     print("Database created!")
    
    app.run(debug=True)
