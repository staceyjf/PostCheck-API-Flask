from flask import current_app
from app.repositories.suburb_repository import repo_get_all_suburbs, repo_get_suburb_by_id, repo_create_suburb
from app.models.models import State

def get_all_suburbs():
    return repo_get_all_suburbs()

def get_suburb_by_id(id):
    maybe_suburb = repo_get_suburb_by_id(id)
    current_app.logger.info(f"get_suburb_by_id is sending back {maybe_suburb}")
    return maybe_suburb

def create_suburb(data):
    # check fields aren't blank
    if not data.get('name'):
        raise ValueError("The 'name' field cannot be blank.")
    if not data.get('state'):
        raise ValueError("The 'state' field cannot be blank.")

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
        raise ValueError(f"{data['state']} is not a valid state. Must be one of: {valid_states}")
    
    # Update to ENUM
    cleaned_data['state'] = state_enum
        
    created_suburb = repo_create_suburb(cleaned_data)
    current_app.logger.info(f"create_suburb is sending back {created_suburb}")

    return created_suburb