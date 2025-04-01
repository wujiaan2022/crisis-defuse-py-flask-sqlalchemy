# scripts/load_topics.py

import json
from flask import current_app
from models import db, Topic
from app import app

def load_topics_from_json(app, filepath="test_data/topics.json"):

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

        with app.app_context():
            print("📦 Using DB:", app.config["SQLALCHEMY_DATABASE_URI"])

            # 🗑️ Delete all existing topics first
            num_deleted = Topic.query.delete()
            print(f"🗑️ Deleted {num_deleted} existing topics.")

            # Add new topics
            for entry in data:
                topic = Topic(
                    slug=entry["slug"],
                    title=entry["title"],
                    content=entry["content"]
                )
                db.session.add(topic)

            db.session.commit()
            print(f"✅ Loaded {len(data)} topics from {filepath}.")

    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error while loading topics: {e}")
