from app.extensions import db
from app.models.models import Suburb


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

    print("this is state before")
    print(updated_data['state'])

    if 'name' in updated_data:
        updated_suburb.name = updated_data['name']

    if 'state' in updated_data:
        updated_suburb.state = updated_data['state']

    print("this is state after")
    print(updated_suburb.state)

    db.session.commit()
    return updated_suburb
