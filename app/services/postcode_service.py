from flask import current_app
from app.repositories.postcode_repository import repo_get_all_postcodes, repo_get_postcode_by_id, repo_create_postcode_with_suburbs, repo_delete_by_id, repo_update_by_id
from app.exceptions.CustomErrors import NotFoundException, ValidationError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def get_all_postcodes():
    return repo_get_all_postcodes()

def create_postcode(data):
    # check fields aren't blank
    if not data.get('postcode'):
        raise ValidationError("The 'postcode' field cannot be blank.")

     # basic data cleaning
    cleaned_data = {}
    cleaned_data['postcode'] = data['postcode'].strip()
    
    if len(cleaned_data['postcode']) != 4:
        raise ValidationError("Postcodes need to be 4 digits long")
    
    if not cleaned_data['postcode'].isdigit():
        raise ValidationError("Postcodes should be numerical")
    
    # logic to add suburbs if they have been provided
    suburb_ids = data.get('suburbIds', []) # see if we have ids or provide an empty []
    if suburb_ids:
        cleaned_data['suburbIds'] = data['suburbIds']
    
    try:    
        created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
        current_app.logger.info(f"Create_postcode is sending back {created_postcode}")
        return created_postcode
    except IntegrityError as e:
        raise ValidationError(f"Validation error on creating a postcode: {e}")
    except NoResultFound as e:
        raise NotFoundException(f"Suburb not found: {e}")
        

def get_postcode_by_id(id):
    try:
        found_postcode = repo_get_postcode_by_id(id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {found_postcode}")
        return found_postcode
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")

    
def delete_postcode_by_id(id):
    try:
        repo_delete_by_id(id)
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")

def update_postcode_by_id(updated_data, id):
    try:
        
        # basic data cleaning
        cleaned_data = {}
        if 'name' in updated_data: 
            cleaned_data['name'] = updated_data['name'].strip()
    
        updated_postcode = repo_update_by_id(cleaned_data,id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {updated_postcode}")
        return updated_postcode
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")
    except IntegrityError as e:
        raise ValidationError(f"Validation error on creating postcode: {e}")