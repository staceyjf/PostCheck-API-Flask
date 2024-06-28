from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from app.schemas.user_schema import UserSchema
from app.schemas.user_schema_args import UserSchemaArgs
from app.schemas.token_schema import TokenSchema
from app.services.user_service import get_all_users, authenticate_user, generate_token, signup_user
from app.auth.token_required_decorator import token_required

bp = Blueprint('user', __name__, url_prefix='/api/v1/auth', description="Operations for Authentication")

@bp.route('/user')
class Users(MethodView):
    @token_required 
    @bp.response(200, UserSchema(many=True))  
    def get(self):
        """
        Fetch all users (Protected)

        Retrieves a list of all registered users from the database. This route is protected and requires a valid authentication token.

        #### Responses:
        200: Success - Returns a list of all users.
        401: Unauthorized - If the authentication token is missing or invalid.
        """
        all_users = get_all_users()
        current_app.logger.info(f"All users successfully sent with a count of {len(all_users)} postcodes")
        return all_users
    
@bp.route('/signin')
class Users(MethodView):
    @bp.arguments(UserSchemaArgs)
    @bp.response(201, TokenSchema())  
    def post(self, data):
        """
        User login

        Authenticates a user based on provided credentials and returns an authentication token for accessing protected routes. This route does not require a token.

        Request body:
        - username: String
        - password: String

        #### Responses:
        201: Success - Returns an authentication token.
        401: Unauthorized - If authentication fails due to invalid credentials.
        """
        try:
            user = authenticate_user(data)
            current_app.logger.info("User successfully authenticated")
            token = generate_token(user)
            current_app.logger.info("Token successfully provided")
            return token
        except CustomValidationError as e:  
            current_app.logger.error(f"Authentication failed: {e}")
            abort(401, message=f"Authentication failed: {e}")
            
@bp.route('/signup')
class Users(MethodView):
    @bp.arguments(UserSchemaArgs)
    @bp.response(201, UserSchema())  
    def post(self, data):
        """
        User sign up

        Registers a new user with the provided credentials. This route does not require a token.

        #### Request body:
        - username: String
        - password: String
        - email: String (optional)

        #### Responses:
        201: Success - Returns the newly created user.
        400: Bad Request - If validation of the request body fails.
        500: Internal Server Error - If an unexpected error occurs during user creation.
        """ 
        try:
            user = signup_user(data)
            current_app.logger.info("User was successfully signed up")
            return user
        except CustomValidationError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}')
        except Exception as e:
            current_app.logger.error(f"Error in creating a new user: {e}")
            abort(500, message="Failed to create user")
