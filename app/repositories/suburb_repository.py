from app.extensions import db
from app.models.models import Suburb

def repo_get_all_suburbs():
    return Suburb.query.all() 
    
def repo_get_suburb_by_id(suburb_id):
    found_suburb = Suburb.query.filter_by(id=suburb_id).first()
    return found_suburb

def repo_create_suburb(data):
    new_suburb = Suburb(suburb=data) #check this 
    print(new_suburb)
    db.session.add(new_suburb)
    db.session.commit()
    return new_suburb