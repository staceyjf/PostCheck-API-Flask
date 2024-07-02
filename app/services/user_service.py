
from datetime import datetime, timedelta
import re
from flask import current_app
import jwt
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from app.exceptions.CustomExceptions import ServiceException
from app.repositories.user_repository import (
    repo_create_user,
    repo_find_user_by_username,
    repo_get_all_users,
)
from config import DevelopmentConfig


def get_all_users():
    return repo_get_all_users()


def find_user_by_username(username):
    # TASK: add the ability to sign in via email
    user = repo_find_user_by_username(username)

    if not user:
        raise ServiceException("There was an issue with your login details. Please try again.")

    return user


def authenticate_user(data):
    if not data or not data.get('username'):
        raise ServiceException("Both username and password are required.")
    # To ensure validation failure remain unknown

    user = find_user_by_username(data.get('username'))

    # return true or false
    if check_password_hash(user.password, data.get('password')):
        return user
    else:
        raise ServiceException("There was an issue with your login details. Please try again.")


def generate_token(user):
    # Hash-based Message Authentication Code - same key is used to sign and verify
    token = jwt.encode({
        'public_id': user.public_id,
        'exp': datetime.now() + timedelta(minutes=30),
    }, DevelopmentConfig.SECRET_KEY, algorithm="HS256")
    return {"accessToken": token}


def signup_user(data):
    if len(data.get('password')) < 5:
        raise ServiceException(f"Passwords need to be longer than 5 characters")

    # positive look ahead (doesn't enforce order) to have at least one number and one alphabetic character
    if not re.search(r"(?=.*\d)(?=.*[a-zA-Z])", data.get('password')):
        raise ServiceException(f"Password should contain a mix of characters and numbers")

    # Stolen from stackoverflow
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, data.get('email')):
        raise ServiceException(f"Emails need to be in a valid email format")

    try:
        new_user = repo_create_user(data)
        current_app.logger.info(f"Signup_user is sending back {new_user}")
        return new_user
    except IntegrityError:
        raise ServiceException(f"Username or email needs to be unique. Please try again.")
