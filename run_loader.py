from app import create_app
from scripts.load_scriptures import load_scriptures_from_json

app = create_app()

# 🌟 Let the loader manage the context
load_scriptures_from_json(app)

