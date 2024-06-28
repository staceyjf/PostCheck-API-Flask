from flask import current_app
from app.repositories.user_repository import repo_get_all_users,repo_find_user_by_username, repo_create_user
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from sqlalchemy.exc import IntegrityError
from  werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import jwt
from datetime import datetime, timedelta

def get_all_users():
    return repo_get_all_users()

def find_user_by_username(username):
     # TASK: add the ability to sign in via email
    user = repo_find_user_by_username(username)
    
    if not user:
        raise CustomValidationError("There was an issue with your login details. Please try again.")
    
    return user

def authenticate_user(data):
    if not data or not data.get('username'):
        raise CustomValidationError("Both username and password are required.") # To ensure validation failure remain unknown
    
    user = find_user_by_username(data.get('username'))
    
    # return true or false
    if check_password_hash(user.password, data.get('password')):
        return user
    else:
        raise CustomValidationError("There was an issue with your login details. Please try again.")

def generate_token(user):
    # 30 min validation window
    token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.now() + timedelta(minutes = 30),
        }, Config['SECRET_KEY'], algorithm="HS256") # Hash-based Message Authentication Code - same key is used to sign and verify
    
    return {"accessToken": token}

def signup_user(data):
    try:
        new_user = repo_create_user(data)
        current_app.logger.info(f"Signup_user is sending back {new_user}")
        return new_user
    except IntegrityError as e: 
        raise CustomValidationError(f"There was an issue with your login details. Please try again.")