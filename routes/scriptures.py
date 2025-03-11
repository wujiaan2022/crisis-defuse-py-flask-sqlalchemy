from flask import Blueprint, request, jsonify, abort
from models import db, Scripture

scriptures_bp = Blueprint('scriptures', __name__)

# ✅ Get all scriptures
@scriptures_bp.route('/', methods=['GET'])
def get_all_scriptures():
    scriptures = Scripture.query.all()
    return jsonify([scripture.to_dict() for scripture in scriptures]), 200

# ✅ Get a single scripture by ID
@scriptures_bp.route('/<int:scripture_id>', methods=['GET'])
def get_scripture(scripture_id):
    scripture = Scripture.query.get_or_404(scripture_id)
    return jsonify(scripture.to_dict()), 200

# ✅ Create new scriptures (single or bulk insert)
@scriptures_bp.route('/', methods=['POST'])
def create_scriptures():
    data = request.json

    if not isinstance(data, list):  # If it's a single object, convert to a list
        data = [data]

    scriptures = []
    for item in data:
        if not item.get('name'):
            abort(400, description="Name is required for each scripture.")

        new_scripture = Scripture(
            name=item['name'],
            summary=item.get('summary'),
            introduction=item.get('introduction'),
            precautions=item.get('precautions'),
            daily_recitation=item.get('daily_recitation'),
            prayer_statement=item.get('prayer_statement'),
            video=item.get('video'),
            audio=item.get('audio'),
            text=item.get('text')
        )
        db.session.add(new_scripture)
        scriptures.append(new_scripture)

    db.session.commit()
    return jsonify([scripture.to_dict() for scripture in scriptures]), 201

# ✅ Update an existing scripture
@scriptures_bp.route('/<int:scripture_id>', methods=['PUT'])
def update_scripture(scripture_id):
    scripture = Scripture.query.get_or_404(scripture_id)
    data = request.json

    if not data.get('name'):
        abort(400, description="Name is required.")

    scripture.name = data.get('name', scripture.name)
    scripture.summary = data.get('summary', scripture.summary)
    scripture.introduction = data.get('introduction', scripture.introduction)
    scripture.precautions = data.get('precautions', scripture.precautions)
    scripture.daily_recitation = data.get('daily_recitation', scripture.daily_recitation)
    scripture.prayer_statement = data.get('prayer_statement', scripture.prayer_statement)
    scripture.audio = data.get('audio', scripture.audio)
    scripture.video = data.get('video', scripture.video)
    scripture.text = data.get('text', scripture.text)

    db.session.commit()
    return jsonify(scripture.to_dict()), 200

# ✅ Delete a scripture
@scriptures_bp.route('/<int:scripture_id>', methods=['DELETE'])
def delete_scripture(scripture_id):
    scripture = Scripture.query.get_or_404(scripture_id)
    db.session.delete(scripture)
    db.session.commit()
    return jsonify({"message": f"Scripture {scripture_id} deleted successfully"}), 200
