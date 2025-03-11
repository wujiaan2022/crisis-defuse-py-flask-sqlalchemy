from flask import Blueprint, request, jsonify, abort
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
from utils.helpers import is_valid_email

users_bp = Blueprint('users', __name__)

logging.basicConfig(level=logging.INFO)  # Set up logging

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        abort(400, description="Name, email, and password are required.")

    if not is_valid_email(email):
        abort(400, description="Invalid email format.")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        abort(400, description="Email already in use.")

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201    

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        abort(400, description="Email and password are required.")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    abort(401, description="Invalid credentials")


@users_bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        abort(404, description="User not found.")

    if not user.is_admin:
        abort(403, description="Admin access required.")

    logging.info(f"Admin Access: User {user.id} accessed admin dashboard.")

    return jsonify({"message": "Welcome to the admin dashboard!"}), 200  


# === REST API ROUTES ===

@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.json
    
    if isinstance(data, list):
        users = []
        for item in data:
            if not item.get('name') or not item.get('email') or not item.get('password'):
                abort(400, description="Name, email, and password are required for each user.")
            if not is_valid_email(item['email']):
                abort(400, description="Invalid email format.")
            
            new_user = User(name=item['name'], email=item['email'])
            new_user.set_password(item['password'])
            users.append(new_user)

        db.session.add_all(users)
        db.session.commit()
        
        return jsonify([user.to_dict() for user in users]), 201
    
    else:
        if not data.get('name') or not data.get('email') or not data.get('password'):
            abort(400, description="Name, email, and password are required.")
        if not is_valid_email(data['email']):
            abort(400, description="Invalid email format.")
        
        new_user = User(name=data['name'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201


@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json

    if not data.get('name') or not data.get('email'):
        abort(400, description="Name and email are required.")
    
    if not is_valid_email(data['email']):
        abort(400, description="Invalid email format.")
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
