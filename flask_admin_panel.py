# flask_admin_panel.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Scripture, Blog, Comment, Topic

from flask_login import current_user
from flask import abort

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return abort(403, description="Admins only.")

# Create the admin object (don't bind to app yet)
admin = Admin(name="CrisisDefuse Admin", template_mode="bootstrap4")

def init_admin(app):
    admin.init_app(app)

    # Add your models here
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Scripture, db.session))
    admin.add_view(SecureModelView(Blog, db.session))
    admin.add_view(SecureModelView(Comment, db.session))
    admin.add_view(SecureModelView(Topic, db.session))
