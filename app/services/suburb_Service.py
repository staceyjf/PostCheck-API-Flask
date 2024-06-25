from app.repositories.suburb_repository import repo_get_all_suburbs, repo_get_suburb_by_id, repo_create_suburb
from app.models.models import State
import logging # Task: review a better logging strategy in the config

def get_all_suburbs():
    return repo_get_all_suburbs()

def get_suburb_by_id(id):
    maybe_suburb = repo_get_suburb_by_id(id)
    if not maybe_suburb:
        logging.error(f"There was an error when finding suburb with id: {id} in the db")
        raise Exception("Failed to find suburb with id: {id}")
    
    return maybe_suburb

def create_suburb(data):
    # removing trailing whitespace
    data['name'].strip()
    data['state'].strip() 
    
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
    data['state'] = state_enum
        
    created_suburb = repo_create_suburb(data)
    if not created_suburb:
        logging.error(f"Failed to create a new suburb in the database for state: {data['state']}")
        raise Exception("Failed to create a new suburb in the db")
    
    return created_suburb