from flask import Blueprint, request, jsonify, abort
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
from utils.valid_email_helpers import is_valid_email
import json

admin_bp = Blueprint('admin', __name__)
logging.basicConfig(level=logging.INFO)  # Logging


@admin_bp.route('/', methods=['GET'])
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

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
def create_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        abort(403, description="Admins only.")

    data = request.json
    
    def create_new_user(info):
        if not info.get('name') or not info.get('email') or not info.get('password'):
            abort(400, description="Name, email, and password are required.")
        if not is_valid_email(info['email']):
            abort(400, description="Invalid email format.")
        if User.query.filter_by(email=info['email']).first():
            abort(400, description=f"Email {info['email']} is already in use.")

        user = User(name=info['name'], email=info['email'])
        user.set_password(info['password'])
        return user

    if isinstance(data, list):
        users = [create_new_user(item) for item in data]
        db.session.add_all(users)
        db.session.commit()
        return jsonify([user.to_dict() for user in users]), 201

    else:
        new_user = create_new_user(data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201


# @admin_bp.route('/users', methods=['GET'])
# @jwt_required()
# def get_users():
#     current_user_id = get_jwt_identity()
#     current_user = User.query.get(current_user_id)

#     if not current_user or not current_user.is_admin:
#         abort(403, description="Admins only.")

#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/users', methods=['GET'])
def get_users(): 

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200