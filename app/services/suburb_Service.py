from flask import current_app
from app.repositories.suburb_repository import repo_get_all_suburbs, repo_get_suburb_by_id, repo_create_suburb, repo_delete_by_id, repo_update_by_id
from app.models.models import State
from app.exceptions.CustomErrors import NotFoundException, ValidationError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def get_all_suburbs():
    return repo_get_all_suburbs()

def create_suburb(data):
    # check fields aren't blank
    if not data.get('name'):
        raise ValidationError("The 'name' field cannot be blank.")
    if not data.get('state'):
        raise ValidationError("The 'state' field cannot be blank.")

    # basic data cleaning
    cleaned_data = {}
    cleaned_data['name'] = data['name'].strip()
    cleaned_data['state'] = data['state'].strip().upper()  
    
    # Convert string to ENUM
    state_enum = None
    for state in State:
        if data['state'] == state.value:
            state_enum = state
            break
    
    # TASK: see how i can make ENUM more flexible
    if state_enum is None: 
        valid_states = ', '.join(state.value for state in State)
        raise ValidationError(f"{data['state']} is not a valid state. Must be one of: {valid_states}")
    
    # Update to ENUM
    cleaned_data['state'] = state_enum
    
    try:
        created_suburb = repo_create_suburb(cleaned_data)
        current_app.logger.info(f"create_suburb is sending back {created_suburb}")
        return created_suburb
    except IntegrityError as e:
        raise ValidationError(f"Validation error on creating a suburb: {e}")

def get_suburb_by_id(id):
    try:
        found_suburb = repo_get_suburb_by_id(id)
        current_app.logger.info(f"get_suburb_by_id is sending back {found_suburb}")
        return found_suburb
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")
    
def delete_suburb_by_id(id):
    try:
        repo_delete_by_id(id)
    except NoResultFound:
        raise NotFoundException(f"suburb with id: {id} not found")

def update_suburb_by_id(updated_data, id):
    try:
        
        cleaned_data = {}
        if 'name' in updated_data:
            cleaned_data['name'] = updated_data['name'].strip()
            
        if 'state' in updated_data:
            cleaned_data['state'] = updated_data['state'].strip().upper()
        
        updated_suburb = repo_update_by_id(cleaned_data,id)
        current_app.logger.info(f"Get_suburb_by_id is sending back {updated_suburb}")
        return updated_suburb
    except NoResultFound:
        raise NotFoundException(f"Suburb with id: {id} not found")
    except IntegrityError as e:
        raise ValidationError(f"Validation error on creating suburb: {e}")