from app.extensions import db
from app.models.models import PostCode, Suburb
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError


def repo_get_all_postcodes():
    return PostCode.query.options(joinedload(PostCode.associatedSuburbs)).all()

 # Use join load to populate the assosciated suburbs via the join table
def repo_get_postcode_by_id(postcode_id):
    found_postcode = PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()
    if not found_postcode:
        raise ValueError(f"Postcode with id {id} not found")
    return found_postcode
    
def repo_create_postcode_with_suburbs(data):
    print(data)
    
    # logic to add suburbs
    # TASK: Look into bulk query fetching
    # TASK: Look at Transcation management to rollback if unsuccessful
    new_associatedSuburbs = []
    for suburb_id in data.get('suburbIds', []):
        suburb = Suburb.query.get(suburb_id)  # querying each suburb by id 
        if suburb:
            new_associatedSuburbs.append(suburb)
        else: # TASK: Create custom error
            raise Exception(f"Suburb with id:{suburb_id} not found")
    
    new_postcode = PostCode(postcode=data['postcode'], associatedSuburbs=new_associatedSuburbs)
    
    try:
        db.session.add(new_postcode)
        db.session.commit()
        return new_postcode
    except IntegrityError as e:
        raise ValueError(f"Integrity Error:. {e}")
 
#ORM-enabled update and delete    
def repo_delete_by_id(postcode_id):
    postcode = PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()
    if not postcode:
        raise ValueError(f"Postcode with id {postcode_id} not found")
    db.session.delete(postcode)
    db.session.commit()