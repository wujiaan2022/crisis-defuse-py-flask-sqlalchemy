from models import Scripture, db
from flask import abort

def create_scripture_objects(data_list):
    scriptures = []
    for item in data_list:
        if not item.get('name'):
            abort(400, description="Name is required for each scripture.")

        scripture = Scripture(
            name=item['name'],
            summary=item.get('summary'),
            introduction=item.get('introduction'),
            precautions=item.get('precautions'),
            daily_recitation=item.get('daily_recitation'),
            prayer_statement=item.get('prayer_statement'),
            video=item.get('video'),
            audio=item.get('audio'),
            title=item.get('title', item.get('name')),
            content=item.get('content', 'Content coming soon.')
        )
        db.session.add(scripture)
        scriptures.append(scripture)

    return scriptures
