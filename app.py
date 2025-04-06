import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ Add this block before anything else
from dotenv import load_dotenv
load_dotenv()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_admin_panel import init_admin
from flask_login import LoginManager

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from models import db, User

from routes.users import users_bp
from routes.admin import admin_bp
from routes.scriptures import scriptures_bp
from routes.topics import topics_bp
from routes.blogs import blogs_bp
from routes.errors import errors_bp
from routes.home import home_bp

from routes.auth import auth_bp

# from scripts.load_scriptures import load_scriptures_from_json  # 👈 Required

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    
    print("🧪 SQLAlchemy URI in use:", Config.SQLALCHEMY_DATABASE_URI)
    
    app.config.from_object(Config)

    db.init_app(app)  #This tells Flask-SQLAlchemy to bind the app to the db instance
    
    init_admin(app)
    
    login_manager.init_app(app)

    # Optional: redirect unauthorized users
    login_manager.login_view = "login"  # Set your login route if using one
    
    Migrate(app, db)  # Initialize Flask-Migrate
    
    # ✅ Allow all origins, methods, and headers
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

    # Initialize the JWTManager
    jwt = JWTManager(app)
    
    # Register Blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(scriptures_bp, url_prefix='/scriptures')
    app.register_blueprint(admin_bp, url_prefix='/admin_api')
    app.register_blueprint(blogs_bp, url_prefix='/blogs')
    app.register_blueprint(topics_bp, url_prefix='/topics')
    app.register_blueprint(errors_bp)  # ✅ No prefix for error handlers
    app.register_blueprint(home_bp)    # ✅ No prefix for the home route  
    
    app.register_blueprint(auth_bp)
      
    # @app.cli.command("load-scriptures")
    # def load_scriptures():
    #     """CLI command to load scriptures from JSON."""
    #     load_scriptures_from_json()
    
    return app

# ✅ This is what the CLI needs!
app = create_app()   


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    


if __name__ == "__main__":
    # app = create_app()
    
    # Create the database and tables
    # ✅ Create a fresh database with the current model
    # with app.app_context():
    #     print("🧱 Creating a fresh database...")
    #     db.create_all()
    #     print("✅ Database created!")
    
    app.run(debug=True)
