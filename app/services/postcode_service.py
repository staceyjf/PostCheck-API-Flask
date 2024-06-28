from flask import current_app
from app.repositories.postcode_repository import repo_get_all_postcodes, repo_get_postcode_by_id, repo_create_postcode_with_suburbs, repo_delete_by_id, repo_update_by_id, query_postcode_by_suburbName, query_postcode_name
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def get_all_postcodes():
    return repo_get_all_postcodes()

def create_postcode(data):
    # check fields aren't blank
    if not data.get('postcode'):
        raise CustomValidationError("The 'postcode' field cannot be blank.")

     # basic data cleaning
    cleaned_data = {}
    cleaned_data['postcode'] = data['postcode'].strip()
    
    if len(cleaned_data['postcode']) != 4:
        raise CustomValidationError("Postcodes need to be 4 digits long")
    
    if not cleaned_data['postcode'].isdigit():
        raise CustomValidationError("Postcodes should be numerical")
    
    # logic to add suburbs if they have been provided
    suburb_ids = data.get('suburbIds', []) # see if we have ids or provide an empty []
    if suburb_ids:
        cleaned_data['suburbIds'] = data['suburbIds']
    
    try:    
        created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
        current_app.logger.info(f"Create_postcode is sending back {created_postcode}")
        return created_postcode
    except IntegrityError as e:
        raise CustomValidationError(f"Validation error on creating a postcode: {e}")
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
    # basic data cleaning
    cleaned_data = {}
    if 'name' in updated_data: 
        cleaned_data['name'] = updated_data['name'].strip()
            
    try:
        updated_postcode = repo_update_by_id(cleaned_data,id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {updated_postcode}")
        return updated_postcode
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")
    except IntegrityError as e:
        raise CustomValidationError(f"Validation error on creating postcode: {e}")
    
def fetch_postcodes_by_suburb(data):
    # check fields aren't blank
    if not data['suburb']:
        raise CustomValidationError("Suburb name can't be blank")
    
    try:
        found_postcode = query_postcode_by_suburbName(data)
        current_app.logger.info(f"fetch_postcodes_by_suburb is sending back {found_postcode}")
        return found_postcode
    except NoResultFound:
        raise NotFoundException(f"No postcodes could be found by query name {data['suburb']}")
    except IntegrityError as e:
        raise CustomValidationError(f"Validation error on querying postcode by suburb name: {e}")
        
def fetch_relatedSuburbs_by_postcode(data):
    # check fields aren't blank
    if not data['postcode']:
        raise CustomValidationError("Postcode can't be blank")

    if not data['postcode'].isdigit():
        raise CustomValidationError("Postcodes should be numerical")
    
    try:
        found_postcode = query_postcode_name(data)
        current_app.logger.info(f"fetch_relatedSuburbs_by_postcode is sending back {found_postcode}")
        return found_postcode
    except NoResultFound:
        raise NotFoundException(f"No relating suburbs could be found by query name {data['suburb']}")
    except IntegrityError as e:
        raise CustomValidationError(f"Validation error on querying postcode by name for relating suburbs: {e}")
        