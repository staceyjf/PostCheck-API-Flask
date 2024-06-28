from flask import current_app
from app.repositories.user_repository import repo_get_all_users,repo_find_user_by_username
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from  werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import jwt
from datetime import datetime, timedelta

def get_all_users():
    return repo_get_all_users()

def authenticate_user(data):
    if not data or not data.get('username'):
        raise CustomValidationError("Authentication failed: Both username and password are required.") # To ensure validation failure remain unknown
    
    user = repo_find_user_by_username(data.get('username'))
    
    if not user:
        raise CustomValidationError("Authentication failed: There was an issue with your login details. Please try again.")
    
    # return true or false
    if check_password_hash(user.password, data.get('password')):
        return user
    else:
        raise CustomValidationError("Authentication failed: There was an issue with your login details. Please try again.")

def generate_token(user):
    # 30 min validation window
    token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.now() + timedelta(minutes = 30),
        }, Config['SECRET_KEY'], algorithm="HS256") # Hash-based Message Authentication Code - same key is used to sign and verify
    
    return {"accessToken": token} 