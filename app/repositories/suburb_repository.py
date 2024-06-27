from app.extensions import db
from app.models.models import Suburb, State
from sqlalchemy.exc import IntegrityError

def repo_get_all_suburbs():
    return Suburb.query.all() 
    
def repo_get_suburb_by_id(suburb_id):
    found_suburb = Suburb.query.filter_by(id=suburb_id).first()
    return found_suburb

def repo_create_suburb(data):
    try:
        new_suburb = Suburb(name=data['name'], state=data['state']) # align it to a State ENUM
        db.session.add(new_suburb)
        db.session.commit()
        return new_suburb
    except IntegrityError as e:
        raise ValueError(f"Integrity Error:. {e}")