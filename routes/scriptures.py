from flask import Blueprint, request, jsonify, abort
from models import db, Scripture
from utils.scripture_helpers import create_scripture_objects
from sqlalchemy import or_


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
    if not isinstance(data, list):
        data = [data]

    scriptures = create_scripture_objects(data)
    db.session.commit()
    return jsonify([s.to_dict() for s in scriptures]), 201

# ✅ Update an existing scripture
@scriptures_bp.route('/<int:scripture_id>', methods=['PUT'])
def update_scripture(scripture_id):
    scripture = Scripture.query.get_or_404(scripture_id)
    data = request.json

    if not data.get('name'):
        abort(400, description="Name is required.")

    # ✨ Update fields with fallback to current values
    scripture.name = data.get('name', scripture.name)
    scripture.title = data.get('title', scripture.title)
    scripture.content = data.get('content', scripture.content)
    scripture.summary = data.get('summary', scripture.summary)
    scripture.introduction = data.get('introduction', scripture.introduction)
    scripture.precautions = data.get('precautions', scripture.precautions)
    scripture.daily_recitation = data.get('daily_recitation', scripture.daily_recitation)
    scripture.prayer_statement = data.get('prayer_statement', scripture.prayer_statement)
    scripture.audio = data.get('audio', scripture.audio)
    scripture.video = data.get('video', scripture.video)

    db.session.commit()
    return jsonify(scripture.to_dict()), 200

# ✅ Delete a scripture
@scriptures_bp.route('/<int:scripture_id>', methods=['DELETE'])
def delete_scripture(scripture_id):
    scripture = Scripture.query.get_or_404(scripture_id)
    db.session.delete(scripture)
    db.session.commit()
    return jsonify({"message": f"Scripture {scripture_id} deleted successfully"}), 200


@scriptures_bp.route('/crisis-selection', methods=['GET'])
def get_scriptures_by_crisis():
    crises = request.args.getlist('crises')

    if not crises:
        return jsonify({"error": "At least one crisis is required."}), 400

    # Get 2 foundation scriptures (same for all)
    foundation = Scripture.query.filter_by(type='foundation').limit(2).all()
    foundation_data = [s.to_dict() for s in foundation]

    # Get all other scriptures (type != 'foundation')
    all_others = Scripture.query.filter(Scripture.type != 'foundation').all()

    result = {}

    for crisis in crises:
        main_scriptures = []
        help_scriptures = []

        for s in all_others:
            roles = s.crisis_roles or {}
            role = roles.get(crisis)

            if role == 'main':
                main_scriptures.append(s.to_dict())
            elif role == 'help':
                help_scriptures.append(s.to_dict())

        result[crisis] = {
            "foundation": foundation_data,              # show same 2 foundation
            "main": main_scriptures[:2],                # max 2
            "help": help_scriptures[:2]                 # max 2
        }

    return jsonify(result), 200



# @scriptures_bp.route('/crisis-selection', methods=['GET'])
# def get_scriptures_by_crisis():
#     selected_crises = request.args.getlist("crises")
#     print("🌟 Selected Crises received from frontend:", selected_crises)

#     # Temporary hardcoded test response
#     return jsonify({
#         "scriptures": [
#             "The Heart Sutra (3x/day)",
#             "Medicine Buddha Mantra (7x/day)"
#         ]
#     })


@scriptures_bp.route("/check-scriptures")
def check_scriptures():
    from models import Scripture  # or wherever your model is
    scriptures = Scripture.query.all()
    return {
        "total": len(scriptures),
        "titles": [s.title for s in scriptures]
    }
