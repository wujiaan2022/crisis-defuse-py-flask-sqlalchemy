from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, User, Scripture, Blog, Comment
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate
    
    # Initialize the JWTManager
    jwt = JWTManager()
    jwt.init_app(app)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": str(error)}), 400    

    # Basic health-check route
    @app.route('/')
    def home():
        return {"message": "CrisisDefuse backend is running!"}, 200
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            abort(400, description="Name, email, and password are required.")

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            abort(400, description="Email already in use.")

        # Create the new user
        new_user = User(name=name, email=email)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201    
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            abort(400, description="Email and password are required.")

        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Check if password matches
            # Create a JWT token
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        else:
            abort(401, description="Invalid credentials")
        
    
    @app.route('/admin', methods=['GET'])
    @jwt_required()
    def admin_dashboard():
        # Print out the JWT token for debugging purposes
        print(f"Authorization header: {request.headers.get('Authorization')}")
        
        # Get the current user ID from the JWT token
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  # Debugging line

        # Retrieve the user from the database
        user = User.query.get(current_user_id)

        if user is None:
            abort(404, description="User not found.")  # Debugging line

        print(f"User is admin: {user.is_admin}")  # Debugging line

        # Check if the user is an admin
        if not user.is_admin:
            abort(403, description="Admin access required.")

        # Admin dashboard logic here
        return jsonify({"message": "Welcome to the admin dashboard!"}), 200    


    # === REST API ROUTES ===

    # USERS
    @app.route('/users', methods=['POST'])
    def add_user():
        data = request.json
        
        # Check if the data is a list
        if isinstance(data, list):
            # Validate each user in the list
            users = []
            for item in data:
                if not item.get('name') or not item.get('email') or not item.get('password'):
                    abort(400, description="Name, email, and password are required for each user.")
                if "@" not in item['email']:
                    abort(400, description="Invalid email format.")
                
                # Create a new user and add to the list
                new_user = User(name=item['name'], email=item['email'])
                new_user.set_password(item['password'])  # Make sure to hash the password
                users.append(new_user)

            # Add all users to the database
            db.session.add_all(users)
            db.session.commit()
            
            # Return a list of created users
            return jsonify([user.to_dict() for user in users]), 201
        
        else:
            # If the input is not a list, handle it as a single user
            if not data.get('name') or not data.get('email') or not data.get('password'):
                abort(400, description="Name, email, and password are required.")
            if "@" not in data['email']:
                abort(400, description="Invalid email format.")
            
            new_user = User(name=data['name'], email=data['email'])
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201


    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        user = User.query.get_or_404(id)
        return jsonify(user.to_dict()), 200

    @app.route('/users/<int:id>', methods=['PUT'])
    def update_user(id):
        user = User.query.get_or_404(id)
        data = request.json

        # Validate required fields
        if not data.get('name') or not data.get('email'):
            abort(400, description="Name and email are required.")
        
        if "@" not in data['email']:
            abort(400, description="Invalid email format.")
        
        # Update user fields
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)

        # Check if a new password is provided, and hash it using the set_password method
        if data.get('password'):
            user.set_password(data['password'])  # This will hash the new password

        db.session.commit()  # Save the changes to the database
        
        return jsonify(user.to_dict()), 200


    @app.route('/users/<int:id>', methods=['DELETE'])
    def delete_user(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

    # SCRIPTURES
    @app.route('/scriptures', methods=['GET'])
    def get_scriptures():
        scriptures = Scripture.query.all()
        return jsonify([scripture.to_dict() for scripture in scriptures]), 200

    @app.route('/scriptures', methods=['POST'])
    def add_scriptures():
        data = request.json  # Can be either a single object or a list of objects

        # If it's a single object, make it a list
        if not isinstance(data, list):
            data = [data]  # Wrap it in a list if it's not already a list

        scriptures = []
        for item in data:
            if not item.get('name'):
                abort(400, description="Name is required for each scripture.")
            
            new_scripture = Scripture(
                name=item['name'],
                info=item.get('info'),
                video=item.get('video'),
                audio=item.get('audio'),
                text=item.get('text')
            )
            db.session.add(new_scripture)
            scriptures.append(new_scripture)

        db.session.commit()
        return jsonify([scripture.to_dict() for scripture in scriptures]), 201

    
    @app.route('/scriptures/<int:id>', methods=['GET'])
    def get_scripture(id):
        scripture = Scripture.query.get_or_404(id)
        return jsonify(scripture.to_dict()), 200

    @app.route('/scriptures/<int:id>', methods=['PUT'])
    def update_scripture(id):
        scripture = Scripture.query.get_or_404(id)
        data = request.json  # Fixed to use request.json
        
        if not data.get('name'):
            abort(400, description="Name is required.")
                
        scripture.name = data.get('name', scripture.name)
        scripture.info = data.get('info', scripture.info)
        scripture.audio = data.get('audio', scripture.audio)
        scripture.video = data.get('video', scripture.video)
        scripture.text = data.get('text', scripture.text)
        
        db.session.commit()
        return jsonify(scripture.to_dict()), 200

    @app.route('/scriptures/<int:id>', methods=['DELETE'])
    def delete_scripture(id):
        scripture = Scripture.query.get_or_404(id)
        db.session.delete(scripture)
        db.session.commit()
        return jsonify({"message": "Scripture deleted"}), 200


    # BLOGS
    @app.route('/blogs', methods=['GET'])
    def get_blogs():
        blogs = Blog.query.all()
        return jsonify([blog.to_dict() for blog in blogs]), 200

    @app.route('/blogs', methods=['POST'])
    def add_blog():
        data = request.json
        
        if not data.get('title') or not data.get('content'):
            abort(400, description="Title and content are required.")
        
        new_blog = Blog(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id']
        )
        db.session.add(new_blog)
        db.session.commit()
        return jsonify(new_blog.to_dict()), 201

    @app.route('/blogs/<int:blog_id>/comments', methods=['GET'])
    def get_blog_comments(blog_id):
        comments = Comment.query.filter_by(blog_id=blog_id).all()
        return jsonify([comment.to_dict() for comment in comments]), 200

    @app.route('/blogs/<int:blog_id>/comments', methods=['POST'])
    def add_comment(blog_id):
        data = request.json
        
        if not data.get('content'):
            abort(400, description="Content is required for the comment.")
        
        new_comment = Comment(
            content=data['content'],
            user_id=data['user_id'],
            blog_id=blog_id
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201

    return app
       

if __name__ == "__main__":
    app = create_app()
    
     # Create the database and tables
    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     print("Database created!")
    
    app.run(debug=True)
