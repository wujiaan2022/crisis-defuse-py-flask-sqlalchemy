# flask_admin_panel.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Scripture, Blog, Comment, Topic

from flask import redirect, url_for, request, flash, abort
from flask_login import current_user


class SecureModelView(ModelView):
    def is_accessible(self):
        print("👀 Access check:", current_user.is_authenticated, getattr(current_user, 'is_admin', None))
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        print("🛑 Access denied. Redirecting to login.")
        return redirect(url_for("auth.login", next=request.url))
    

# class SecureModelView(ModelView):
#     def is_accessible(self):        
#         return True  
    

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
