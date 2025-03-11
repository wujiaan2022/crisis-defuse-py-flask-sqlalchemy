from flask import Blueprint, jsonify

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@errors_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400
