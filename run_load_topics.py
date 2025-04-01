from app import create_app
from scripts.load_topics import load_topics_from_json

app = create_app()
load_topics_from_json(app)
