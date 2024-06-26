from app.extensions import db
from app.models.models import PostCode, Suburb

def repo_get_all_postcodes():
    return PostCode.query.all()

def repo_get_postcode_by_id(postcode_id):
    found_postcode = PostCode.query.filter_by(id=postcode_id).first()
    return found_postcode 
    
def repo_create_postcode_with_suburbs(data):
    print(data)
    new_postcode = PostCode(postcode=data['postcode'], associatedSuburbs=data['associatedSuburbs'])
    db.session.add(new_postcode)
    db.session.commit()
    return new_postcode