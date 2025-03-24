import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from models import db

from routes.users import users_bp
from routes.scriptures import scriptures_bp
from routes.blogs import blogs_bp
from routes.errors import errors_bp
from routes.home import home_bp

# from scripts.load_scriptures import load_scriptures_from_json  # 👈 Required


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
      
    # @app.cli.command("load-scriptures")
    # def load_scriptures():
    #     """CLI command to load scriptures from JSON."""
    #     load_scriptures_from_json()
    
    return app

# ✅ This is what the CLI needs!
app = create_app()       

if __name__ == "__main__":
    app = create_app()
    
    # Create the database and tables
    # ✅ Create a fresh database with the current model
    # with app.app_context():
    #     print("🧱 Creating a fresh database...")
    #     db.create_all()
    #     print("✅ Database created!")
    
    app.run(debug=True)
