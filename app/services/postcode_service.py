from flask import current_app
from app.repositories.postcode_repository import repo_get_all_postcodes, repo_get_postcode_by_id, repo_create_postcode_with_suburbs, repo_delete_by_id

def get_all_postcodes():
    return repo_get_all_postcodes()

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
    suburb_ids = data.get('suburbIds', []) # see if we have ids or provide an empty []
    print(suburb_ids)
    if suburb_ids:
        cleaned_data['suburbIds'] = data['suburbIds']
    
    try:    
        created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
        current_app.logger.info(f"Create_postcode is sending back {created_postcode}")
        return created_postcode
    except ValueError as e:
        current_app.logger.error(f"Error when creating the postcode in the db: {e}")
        raise ValueError(f"Field needs to be unique")

def get_postcode_by_id(id):
    try:
        found_postcode = repo_get_postcode_by_id(id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {found_postcode}")
        return found_postcode
    except ValueError as e:
        error_message = f"Postcode with id:{id} not found"
        current_app.logger.error(f"{error_message}: {e}")
        raise ValueError(error_message)
    
def delete_postcode_by_id(id):
    try:
        repo_delete_by_id(id)
    except ValueError as e:
        error_message = f"Postcode with id:{id} not found when trying to delete"
        current_app.logger.error(f"{error_message}: {e}")
        raise ValueError(error_message)