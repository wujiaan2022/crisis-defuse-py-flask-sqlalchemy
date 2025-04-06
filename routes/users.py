from flask import Blueprint, request, jsonify, abort
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
from utils.valid_email_helpers import is_valid_email
import json

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

    # ✅ Generate JWT token after registration
    access_token = create_access_token(identity=new_user.id)

    # ✅ Send token and name to frontend
    return jsonify(access_token=access_token, name=new_user.name), 201    


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
        return jsonify(access_token=access_token, name=user.name), 200

    abort(401, description="Invalid credentials")
    
    
@users_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    current_user = User.query.get(get_jwt_identity())

    # Allow access if it's self or if user is admin
    if not current_user or (current_user.id != id and not current_user.is_admin):
        abort(403, description="You can only view your own profile unless you're an admin.")

    user = User.query.get_or_404(id)
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
    current_user = User.query.get(get_jwt_identity())
    
    # Only allow if user is updating their own profile OR admin
    if not current_user or (current_user.id != id and not current_user.is_admin):
        abort(403, description="You can only update your own profile unless you're an admin.")

    user = User.query.get_or_404(id)
    data = request.json
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']

    db.session.commit()
    return jsonify(user.to_dict()), 200


@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user = User.query.get(get_jwt_identity())
    
    if not current_user or (current_user.id != id and not current_user.is_admin):
        abort(403, description="You can only delete your own account unless you're an admin.")

    user = User.query.get_or_404(id)
    
     # ✅ Log this critical action
    logging.info(f"User {current_user.id} deleted user {id}")
    
    db.session.delete(user)
    db.session.commit()
    return jsonify(message=f"User {id} deleted successfully"), 200


