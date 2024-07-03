from flask import current_app, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.exceptions.CustomExceptions import ServiceException
from app.services.report_service import process_property_data
# from app.auth.token_required_decorator import token_required

bp = Blueprint('reporting', __name__, url_prefix='/api/v1/reporting', description="Operations on reporting")


@bp.route('/')
class Report(MethodView):
    # @token_required
    def get(self):
        """
        Fetch pricing reporting for properties (Protected)

        Retrieves the average price by state across a time.

        #### Responses
        - 200: Success - Returns avg property proerties by state across time.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 500: Internal Server Error - If an unexpected error occurs during data processing.
        """
        try:
            # TASK: review a better approach than pagination for managing loading
            all_data = process_property_data()
            current_app.logger.info(f"Avg price by state data has been successfully read")
            # manual serialise the data
            return jsonify(all_data), 200
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message="There was an issue while processing the report data. Please try again later.")
        except Exception as e:
            current_app.logger.error(f"Error in processing the reporting data: {e}")
            abort(500, message="There was an issues while processing the report data. Please try again later.")
