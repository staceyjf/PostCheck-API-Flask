from app.extensions import db
from app.models.models import PostCode, Suburb
from sqlalchemy.orm import joinedload


def repo_get_all_postcodes():
    return PostCode.query.options(joinedload(PostCode.associatedSuburbs)).order_by(PostCode.postcode).all()


# Use join load to populate the associated suburbs via the join table
def repo_get_postcode_by_id(postcode_id):
    return PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()


def repo_create_postcode_with_suburbs(data):
    # TASK: Look at Transcation management to rollback if unsuccessful

    suburb_ids = data.get('suburbIds', [])
    suburbs = Suburb.query.filter(Suburb.id.in_(suburb_ids)).all()  # bulk query fetching

    new_postcode = PostCode(postcode=data['postcode'], associatedSuburbs=suburbs)
    db.session.add(new_postcode)
    db.session.commit()
    return new_postcode


# ORM-enabled update and delete
def repo_delete_by_id(postcode_id):
    postcode = PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()
    db.session.delete(postcode)
    db.session.commit()


def repo_update_by_id(updated_data, postcode_id):
    updated_postcode = PostCode.query.options(joinedload(PostCode.associatedSuburbs)).filter_by(id=postcode_id).first()

    if 'postcode' in updated_data:
        updated_postcode.postcode = updated_data['postcode']

    print(updated_data)

    if 'suburbIds' in updated_data:
        updated_postcode.associatedSuburbs.clear()  # clear the associations to rest
        suburb_ids = updated_data.get('suburbIds', [])
        suburbs = Suburb.query.filter(Suburb.id.in_(suburb_ids)).all()
        updated_postcode.associatedSuburbs = suburbs

    db.session.commit()
    return updated_postcode


def query_postcodes_by_suburbName(data):
    search_pattern = f"%{data['suburb']}%"

    found_postcodes = db.session.query(PostCode).join(PostCode.associatedSuburbs) \
        .filter(Suburb.name.ilike(search_pattern)) \
        .options(joinedload(PostCode.associatedSuburbs)) \
        .all()
    print(found_postcodes)
    return found_postcodes or []


def query_postcodes_name(data):
    search_pattern = f"%{data['postcode']}%"

    found_postcodes = db.session.query(PostCode).filter(PostCode.postcode.ilike(search_pattern)) \
        .options(joinedload(PostCode.associatedSuburbs)).all()
    print(found_postcodes)
    return found_postcodes or []
