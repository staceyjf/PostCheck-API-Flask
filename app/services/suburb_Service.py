from app.repositories.suburb_repository import repo_get_all_suburbs, repo_get_suburb_by_id, repo_create_suburb
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
    created_suburb = repo_create_suburb(data)
    if not created_suburb:
        logging.error(f"There was an error in creating a new suburb in the db")
        raise Exception("Failed to create a new suburb")
    
    return created_suburb