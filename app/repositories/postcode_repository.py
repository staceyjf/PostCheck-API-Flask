from app.extensions import db
from app.models.models import PostCode, Suburb
from sqlalchemy.orm import joinedload


def repo_get_all_postcodes():
    return PostCode.query.options(joinedload(PostCode.associatedSuburbs)).all()

 # Use join load to populate the assosciated suburbs via the join table
def repo_get_postcode_by_id(postcode_id):
    found_postcode = PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()
    return found_postcode
    
def repo_create_postcode_with_suburbs(data):
    print(data)
    
    # logic to add suburbs
    new_associatedSuburbs = []
    for suburb_id in data['suburbIds']:
        suburb = Suburb.query.get(suburb_id)  # querying each suburb by id 
        if suburb:
            new_associatedSuburbs.append(suburb)
        else:
            raise Exception(f"Suburb with id:{suburb_id} not found")
    
    new_postcode = PostCode(postcode=data['postcode'], associatedSuburbs=new_associatedSuburbs)
    db.session.add(new_postcode)
    db.session.commit()
    return new_postcode