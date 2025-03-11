from flask import Blueprint, request, jsonify, abort
from models import db, Blog, Comment

blogs_bp = Blueprint('blogs', __name__)

# ✅ Get all blogs
@blogs_bp.route('/', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs]), 200

# ✅ Create a new blog
@blogs_bp.route('/', methods=['POST'])
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

# ✅ Get all comments for a specific blog
@blogs_bp.route('/<int:blog_id>/comments', methods=['GET'])
def get_blog_comments(blog_id):
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    return jsonify([comment.to_dict() for comment in comments]), 200

# ✅ Add a comment to a specific blog
@blogs_bp.route('/<int:blog_id>/comments', methods=['POST'])
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
