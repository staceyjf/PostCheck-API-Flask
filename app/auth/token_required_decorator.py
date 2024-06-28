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
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return abort(401, message="Token is missing.")
        
        try:
            # decoding to fetch the payload
            data = jwt.decode(token, Config.SECRET_KEY)
            # find the user by public_id
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return abort(401, message="Token is invalid.")
        
        # returns the current logged in user context to the controller
        return f(current_user, *args, **kwargs)
    
    return decorated