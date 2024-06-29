import jwt  # imports for PyJWT authentication
from flask import request
from flask_smorest import abort
from config import Config
# from app.models.models import User  # Commented out since it's not used
from functools import wraps


# Decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
        if not token:
            return abort(401, message="Token is missing.")
        # Decoding to fetch the payload
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
            # Find the user by public_id approach is causing errors
            # route requests so have commented it out for now
            # current_user = User.query.
            # filter_by(public_id=data['public_id']).first()
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return abort(401, message="Token is invalid.")
        except Exception:
            return abort(401,
                         message="There is an issue with Token validation.")
        return f(*args, **kwargs)
    return decorated
