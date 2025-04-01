from flask import Blueprint, jsonify
from models import Topic

topics_bp = Blueprint('topics', __name__)

@topics_bp.route("/", methods=["GET"])
def get_all_topics():
    topics = Topic.query.all()
    return jsonify([t.to_dict() for t in topics])

@topics_bp.route("/<slug>", methods=["GET"])
def get_topic(slug):
    topic = Topic.query.filter_by(slug=slug).first()
    if topic:
        return jsonify(topic.to_dict())
    return jsonify({"error": "Topic not found"}), 404
