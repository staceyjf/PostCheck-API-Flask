from app.extensions import db
from app.models.models import PostCode, Suburb
from sqlalchemy.orm import joinedload


def repo_get_all_suburbs():
    return Suburb.query.all()


def repo_get_suburb_by_id(suburb_id):
    return Suburb.query.filter_by(id=suburb_id).first()


def repo_create_suburb(data):
    new_suburb = Suburb(name=data['name'], state=data['state'])
    db.session.add(new_suburb)
    db.session.commit()
    return new_suburb


# ORM-enabled update and delete
def repo_delete_by_id(suburb_id):
    suburb = Suburb.query.filter_by(id=suburb_id).first()
    db.session.delete(suburb)
    db.session.commit()


def repo_update_by_id(updated_data, suburb_id):
    updated_suburb = Suburb.query.filter_by(id=suburb_id).first()

    if 'name' in updated_data:
        updated_suburb.name = updated_data['name']

    if 'state' in updated_data:
        updated_suburb.state = updated_data['state']

    db.session.commit()
    return updated_suburb


def query_suburbs_by_postcodeValue(data):
    search_pattern = f"%{data['postcode']}%"

    found_postcodes = db.session.query(Suburb).join(Suburb.associatedPostCodes) \
        .filter(PostCode.postcode.ilike(search_pattern)) \
        .options(joinedload(Suburb.associatedPostCodes)) \
        .all()
    return found_postcodes or []
