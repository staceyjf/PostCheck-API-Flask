from app.repositories.postcode_repository import repo_get_all_postcodes, repo_get_postcode_by_id, repo_create_postcode_with_suburbs
from app.services.suburb_Service import get_suburb_by_id
import logging # Task: review a better logging strategy in the config


def get_all_postcodes():
    return repo_get_all_postcodes()

def get_postcode_by_id(id):
    maybe_postcode = repo_get_postcode_by_id(id)

    return maybe_postcode

def create_postcode(data):
     # basic data cleaning
    cleaned_data = {}
    cleaned_data['postcode'] = data['postcode'].strip()
    
    if len(cleaned_data['postcode']) != 4:
        raise ValueError("Postcodes need to be 4 digits long")
    
    if not cleaned_data['postcode'].isdigit():
        raise ValueError("Postcodes should be numerical")
    
    # logic to add suburbs
    new_associatedSuburbs = []
    for suburb_id in data['suburbIds']:
        suburb = get_suburb_by_id(suburb_id)
        if suburb:
            new_associatedSuburbs.append(suburb)
        else:
            raise Exception(f"Suburb with id:{suburb_id} not found")
    
    # add the suburbs to our dict
    cleaned_data['associatedSuburbs'] = new_associatedSuburbs
        
    created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
    if not created_postcode:
        logging.error(f"There was an error in creating a new postcode in the db")
        raise Exception("Failed to create a new todo")
    
    return created_postcode