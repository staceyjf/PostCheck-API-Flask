from flask import current_app
from app.repositories.user_repository import repo_get_all_users
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

def get_all_users():
    return repo_get_all_users()