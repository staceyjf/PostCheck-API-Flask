from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError
from app.schemas.user_schema import UserSchema
from app.services.user_service import get_all_users

bp = Blueprint('user', __name__, url_prefix='/api/v1/auth', description="Operations for Authentication")

@bp.route('/')
class Users(MethodView):
    @bp.response(200, UserSchema(many=True))  
    def get(self):
        """Fetch all users

        Retrieves a list of all users from the database.
        """
        all_users = get_all_users()
        current_app.logger.info(f"All postcodes successful sent with a count of {len(all_users)} postcodes")
        return all_users