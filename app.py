from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, User, Scripture, Blog, Comment


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate

    # Basic health-check route
    @app.route('/')
    def home():
        return {"message": "CrisisDefuse backend is running!"}, 200

    # === REST API ROUTES ===

    # USERS
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200

    @app.route('/users', methods=['POST'])
    def add_user():
        data = request.json
        new_user = User(name=data['name'], email=data['email'])
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
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
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
    def add_scripture():
        data = request.json
        new_scripture = Scripture(
            name=data['name'],
            info=data.get('info'),
            video=data.get('video'),
            audio=data.get('audio'),
            text=data.get('text')
        )
        db.session.add(new_scripture)
        db.session.commit()
        return jsonify(new_scripture.to_dict()), 201

    # BLOGS
    @app.route('/blogs', methods=['GET'])
    def get_blogs():
        blogs = Blog.query.all()
        return jsonify([blog.to_dict() for blog in blogs]), 200

    @app.route('/blogs', methods=['POST'])
    def add_blog():
        data = request.json
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

    # Uncomment this block to create tables if not using Flask-Migrate yet
    # with app.app_context():
    #     print("Creating database...")
    #     db.create_all()
    #     print("Database created!")

    app.run(debug=True)
