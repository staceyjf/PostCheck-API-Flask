from app.extensions import db
from app.models.models import PostCode, Suburb

def repo_get_all_postcodes():
        return PostCode.query.all() 
    
def repo_create_postcode_with_suburbs(data):
    new_postcode = PostCode(postcode=data)
    db.session.add(new_postcode)
    db.session.commit()
    return new_postcode