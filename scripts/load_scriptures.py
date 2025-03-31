import json
from models import db, Scripture  # Make sure models.py is in the root folder
from utils.scripture_helpers import create_scripture_objects  # Reuses your validation logic
from flask import current_app
from app import app


def load_scriptures_from_json(app, filepath="test_data/scriptures.json"):

    from models import Scripture  # (import inside to avoid circular import)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

        with app.app_context():
            
            print("📦 Using DB:", app.config["SQLALCHEMY_DATABASE_URI"])  # 🧪 Confirm!
            # ❗️ Delete all existing scriptures
            num_deleted = Scripture.query.delete()
            print(f"🗑️ Deleted {num_deleted} existing scriptures.")

            # Add new ones
            scriptures = create_scripture_objects(data)
            db.session.commit()
            print(f"✅ Loaded {len(scriptures)} new scriptures from {filepath}.")

    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error while loading scriptures: {e}")
