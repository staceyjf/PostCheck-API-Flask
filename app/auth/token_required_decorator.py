import jwt # imports for PyJWT authentication
from flask import request
from flask_smorest import abort
from config import Config
from app.models.models import User
from functools import wraps

# decorator for varifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return abort(401, message="Token is missing.")
        
        # decoding to fetch the payload
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
            # current_user = User.query.filter_by(public_id = data['public_id']).first() # find the user by public_id
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
            return abort(401, message="Token is invalid.")
        except:
            return abort(401, message="There is an issue with the Token validation.")
        
        # removed the user to see if this is the issue
        return f(*args, **kwargs)
    
    return decorated