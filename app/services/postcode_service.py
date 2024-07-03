from flask import current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app.exceptions.CustomExceptions import NotFoundException, ServiceException, DbValidationError
from app.repositories.postcode_repository import (
    query_postcodes_by_suburbName,
    query_postcodes_name,
    repo_create_postcode_with_suburbs,
    repo_delete_by_id,
    repo_get_all_postcodes,
    repo_get_postcode_by_id,
    repo_update_by_id,
)


def get_all_postcodes():
    return repo_get_all_postcodes()


def create_postcode(data):
    # basic validation
    if not data.get('postcode'):
        raise ServiceException("The 'postcode' field cannot be blank.")

    # basic data cleaning
    cleaned_data = {}
    cleaned_data['postcode'] = data['postcode'].strip()

    if cleaned_data['postcode'] == "":
        raise ServiceException("Postcodes need to contain a value")

    if len(cleaned_data['postcode']) != 4:
        raise ServiceException("Postcodes need to be 4 digits long")

    if not cleaned_data['postcode'].isdigit():
        raise ServiceException("Postcodes should be numerical")

    # logic to add suburbs if they have been provided
    suburb_ids = data.get('suburbIds', [])  # see if we have ids or provide an empty []
    if suburb_ids:
        cleaned_data['suburbIds'] = data['suburbIds']

    try:
        created_postcode = repo_create_postcode_with_suburbs(cleaned_data)
        current_app.logger.info(f"Create_postcode is sending back {created_postcode}")
        return created_postcode
    except IntegrityError as e:
        error_message = str(e.orig)
        if "Duplicate entry" in error_message:
            raise DbValidationError(f"Postcodes need to have unique names")
        if "NOT NULL" in error_message:
            raise DbValidationError(f"Postcodes need to have an input value")
    except NoResultFound as e:
        raise NotFoundException(f"Suburb not found: {e}")


def get_postcode_by_id(id):
    try:
        found_postcodes = repo_get_postcode_by_id(id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {found_postcodes}")
        return found_postcodes
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")


def delete_postcode_by_id(id):
    try:
        repo_delete_by_id(id)
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")


def update_postcode_by_id(updated_data, id):
    print(updated_data)
    # basic data cleaning
    cleaned_data = {}
    if 'postcode' in updated_data:
        cleaned_data['postcode'] = updated_data['postcode'].strip()

    if 'suburbIds' in updated_data:
        cleaned_data['suburbIds'] = updated_data['suburbIds']

    try:
        updated_postcode = repo_update_by_id(cleaned_data, id)
        current_app.logger.info(f"Get_postcode_by_id is sending back {updated_postcode}")
        return updated_postcode
    except NoResultFound:
        raise NotFoundException(f"Postcode with id: {id} not found")
    except IntegrityError as e:
        raise ServiceException(f"{e}")


def fetch_postcodes_by_suburb(data):
    # basic validation
    if not data['suburb']:
        raise ServiceException("Suburb name can't be blank")

    try:
        found_postcodes = query_postcodes_by_suburbName(data)
        current_app.logger.info(f"fetch_postcodes_by_suburb is sending back {found_postcodes}")
        return found_postcodes
    except IntegrityError as e:
        raise ServiceException(f"{e}")


def fetch_relatedSuburbs_by_postcode(data):
    # basic validation
    if not data['postcode']:
        raise ServiceException("Postcode can't be blank")

    if not data['postcode'].isdigit():
        raise ServiceException("Postcodes should be numerical")

    try:
        found_postcodes = query_postcodes_name(data)
        current_app.logger.info(f"fetch_relatedSuburbs_by_postcode is sending back {found_postcodes}")
        return found_postcodes
    except IntegrityError as e:
        raise ServiceException(f"{e}")
