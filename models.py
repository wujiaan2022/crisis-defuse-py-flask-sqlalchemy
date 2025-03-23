from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

# Association Table for Many-to-Many Relationship (User <-> Scripture)
user_scriptures = db.Table(
    'user_scriptures',  # Specifies the table name in the database
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),  # Foreign key linking to user's id
    db.Column('scripture_id', db.Integer, db.ForeignKey('scriptures.id'), primary_key=True)  # Foreign key linking to scripture's id
)


class User(db.Model):
    __tablename__ = 'users'  # Specifies the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each user
    name = db.Column(db.String(100), nullable=False)  # User's name
    email = db.Column(db.String(120), unique=True, nullable=False)  # User's email address
    password_hash = db.Column(db.String(128), nullable=False)
    
    is_admin = db.Column(db.Boolean, default=False, nullable=True)  # New field, default is False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # One-to-Many relationship: A user can have multiple blogs
    blogs = db.relationship('Blog', backref='author', lazy=True)

    # Many-to-Many relationship: A user can save multiple scriptures
    scriptures = db.relationship(
        'Scripture',
        secondary='user_scriptures',  # Association table
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "blogs": [blog.to_dict() for blog in self.blogs],  # Include related blogs
            "scriptures": [{"id": s.id, "name": s.name} for s in self.scriptures]  # Simplified scripture data
        }


class Scripture(db.Model):
    __tablename__ = 'scriptures'  # Specifies the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each scripture
    name = db.Column(db.String(150), nullable=False)  # Name of the scripture
    summary = db.Column(db.Text)  # Short summary (1-2 sentences)
    introduction = db.Column(db.Text)  # Detailed introduction
    precautions = db.Column(db.Text)  # Precautions to follow
    daily_recitation = db.Column(db.Text)  # Recommended daily recitation count
    prayer_statement = db.Column(db.Text)  # Specific prayer statement
    video = db.Column(db.String(200))  # URL or path to a related video
    audio = db.Column(db.String(200))  # URL or path to a related audio file
    title = db.Column(db.String(200), nullable=True)  # Short, searchable
    content = db.Column(db.Text, nullable=True)       # Long scripture body

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "summary": self.summary,
            "introduction": self.introduction,
            "precautions": self.precautions,
            "daily_recitation": self.daily_recitation,
            "prayer_statement": self.prayer_statement,
            "video": self.video,
            "audio": self.audio,
            "title": self.title,
            "content": self.content,            
        }



class Blog(db.Model):
    __tablename__ = 'blogs'  # Specifies the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each blog post
    title = db.Column(db.String(200), nullable=False)  # Title of the blog post
    content = db.Column(db.Text, nullable=False)  # Content of the blog post
    likes = db.Column(db.Integer, default=0)  # Number of likes; defaults to 0
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to the user's id

    # One-to-Many relationship: A blog can have multiple comments
    comments = db.relationship('Comment', backref='blog', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "likes": self.likes,
            "comments": [comment.to_dict() for comment in self.comments]  # Include related comments
        }


class Comment(db.Model):
    __tablename__ = 'comments'  # Specifies the table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each comment
    content = db.Column(db.Text, nullable=False)  # Content of the comment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking to the comment author's id
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)  # Foreign key linking to the blog post's id

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "blog_id": self.blog_id
        }
