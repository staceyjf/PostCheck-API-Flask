from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from app.schemas.user_schema import UserSchema
from app.schemas.user_schema_args import UserSchemaArgs
from app.schemas.token_schema import TokenSchema
from app.services.user_service import get_all_users, authenticate_user, generate_token
from app.auth.token_required_decorator import token_required

bp = Blueprint('user', __name__, url_prefix='/api/v1/auth', description="Operations for Authentication")

@bp.route('/user')
class Users(MethodView):
    # @token_required 
    @bp.response(200, UserSchema(many=True))  
    def get(self):
        """
        Fetch all users

        Retrieves a list of all registered users from the database. This route is protected and requires a valid authentication token.
        """
        all_users = get_all_users()
        current_app.logger.info(f"All users successfully sent with a count of {len(all_users)} postcodes")
        return all_users
    
@bp.route('/login')
class Users(MethodView):
    @bp.arguments(UserSchemaArgs)
    @bp.response(201, TokenSchema())  
    def post(self, data):
        """
        User login

        Authenticates a user based on provided credentials and returns an authentication token for accessing protected routes. This route does not require a token.
        """ 
        try:
            user = authenticate_user(data)
            current_app.logger.info("User successfully authenticated")
            token = generate_token(user)
            current_app.logger.info("Token successfully provided")
            return token
        except CustomValidationError as e:  
            current_app.logger.error(f"Authentication failed: {str(e)}")
            abort(401, message=f"Authentication failed: {e}")
