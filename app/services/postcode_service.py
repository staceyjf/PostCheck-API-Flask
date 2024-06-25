from app.repositories.postcode_repository import repo_get_all_postcodes, repo_create_postcode_with_suburbs
from app.services.suburb_Service import get_suburb_by_id
import logging # Task: review a better logging strategy in the config


def get_all_postcodes():
    return repo_get_all_postcodes()

def create_postcode(data):
    if len(data.postcode) != 4:
        raise ValueError(f"Postcodes need to be 4 digits long")
    
    if not data.postcode.isdigit():
        raise ValueError(f"Postcode need to only contain numbers")
    
    # logic to add suburbs
    new_associatedSuburbs = []
    for suburb_id in data.suburbIds:
        suburb = get_suburb_by_id(suburb_id)
        if suburb:
            new_associatedSuburbs.append(suburb)
        else:
            raise Exception(f"Suburb with id:{suburb_id} not found")
    
    # replace the old suburbs    
    data.associatedSuburbs = new_associatedSuburbs
        
    created_postcode = repo_create_postcode_with_suburbs(data)
    if not created_postcode:
        logging.error(f"There was an error in creating a new todo in the db")
        raise Exception("Failed to create a new todo")
    
    return created_postcode