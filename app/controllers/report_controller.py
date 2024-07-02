from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.exceptions.CustomExceptions import ServiceException
from app.services.report_service import process_property_data
from app.schemas.reporting_schema import ReportSchema
# from app.auth.token_required_decorator import token_required

bp = Blueprint('reporting', __name__, url_prefix='/api/v1/reporting', description="Operations on reporting")


# GET /pets/?page=2&page_size=10 example endpoint
@bp.route('/')
class Report(MethodView):
    # @token_required
    @bp.response(200, ReportSchema(many=True))
    # @bp.paginate()
    def get(self):
        """
        Fetch pricing reporting for properties
        Retrieves the average price by state across a time (dataset was from '18 to '21)
        #### Responses
        200: Success - Returns avg property proerties by state across time.
        401: Unauthorized - If the authentication token is missing or invalid.
        500: Internal Server Error - If an unexpected error occurs during data processing.
        """
        try:
            all_data = process_property_data()
            # pagination logic for smorest
            current_app.logger.info(f"Avg price by state data has been successfully read")
            return all_data
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message="There was an issue while processing the report data. Please try again later.")
        except Exception as e:
            current_app.logger.error(f"Error in processing the reporting data: {e}")
            abort(500, message="There was an issues while processing the report data. Please try again later.")
