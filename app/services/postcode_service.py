from flask import current_app
from app.repositories.postcode_repository import repo_get_all_postcodes, repo_get_postcode_by_id, repo_create_postcode_with_suburbs
from app.services.suburb_Service import get_suburb_by_id

def get_all_postcodes():
    return repo_get_all_postcodes()

def get_postcode_by_id(id):
    maybe_postcode = repo_get_postcode_by_id(id)
    current_app.logger.info(f"Get_postcode_by_id is sending back {maybe_postcode}")
    return maybe_postcode

def create_postcode(data):
    # check fields aren't blank
    if not data.get('postcode'):
        raise ValueError("The 'postcode' field cannot be blank.")

     # basic data cleaning
    cleaned_data = {}
    cleaned_data['postcode'] = data['postcode'].strip()
    
    if len(cleaned_data['postcode']) != 4:
        raise ValueError("Postcodes need to be 4 digits long")
    
    if not cleaned_data['postcode'].isdigit():
        raise ValueError("Postcodes should be numerical")
    
    # logic to add suburbs if they have been provided
    suburb_ids = data.get('suburbIds')
    print(suburb_ids)
    if suburb_ids is not None and len(suburb_ids) != 0:
    #     new_associatedSuburbs = []
    #     for suburb_id in data['suburbIds']:
    #         suburb = get_suburb_by_id(suburb_id)
    #         if suburb:
    #             print(f"Suburb ID: {suburb.id}, Name: {suburb.name}")
    #             new_associatedSuburbs.append(suburb)
    #         else:
    #             raise Exception(f"Suburb with id:{suburb_id} not found")
    
    #     # add the suburbs to our dict
    #     cleaned_data['associatedSuburbs'] = new_associatedSuburbs
        cleaned_data['suburbIds'] = data['suburbIds']
        
    created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
    current_app.logger.info(f"Create_postcode is sending back {created_postcode}")

    return created_postcode