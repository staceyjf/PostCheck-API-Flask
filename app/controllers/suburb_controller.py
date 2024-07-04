from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.auth.token_required_decorator import token_required
from app.exceptions.CustomExceptions import NotFoundException, DbValidationError, ServiceException
from app.schemas.suburb_schema import SuburbSchema
from app.schemas.suburb_schema_args import SuburbSchemaArgs, SuburbSchemaBySuburbName
from app.services.suburb_service import (
    create_suburb, delete_suburb_by_id, get_all_suburbs,
    get_suburb_by_id, update_suburb_by_id, fetch_suburbs_by_postcode
)


bp = Blueprint('suburb', __name__, url_prefix='/api/v1/suburbs', description="Operations on suburbs")


@bp.route('/')
class Suburbs(MethodView):
    @bp.response(200, SuburbSchema(many=True))
    def get(self):
        """
        Fetch all suburbs

        Retrieves a list of all suburbs from the database.

        ### Responses
        - 200: Success - Returns a list of all suburbs.
        """
        all_suburbs = get_all_suburbs()
        current_app.logger.info(f"All suburbs successfully sent with a count of {len(all_suburbs)} suburbs")
        return all_suburbs

    @token_required
    @bp.arguments(SuburbSchemaArgs)
    @bp.response(201, SuburbSchema())
    def post(self, data):
        """
        Create a new suburb (Protected)

        Creates a new suburb with the provided data. This endpoint is protected and requires Bearer Authentication.

        ### Request Body
        - `name`: String, required
        - `state`: String, required

        ### Responses
        - 201: Success - Returns the newly created suburb.
        - 400: Bad Request - If validation of the request body fails.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 500: Internal Server Error - If an unexpected error occurs during suburb creation.
        """
        try:
            new_suburb = create_suburb(data)
            current_app.logger.info(f"Created suburb: {new_suburb}")
            return new_suburb
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'{e}')
        except DbValidationError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'{e}')
        except Exception as e:
            current_app.logger.error(f"Error in a new suburb: {e}")
            abort(500, message="Failed to create suburb")


@bp.route('/query')
class SuburbQueries(MethodView):
    @bp.arguments(SuburbSchemaBySuburbName, location="query")
    @bp.response(200, SuburbSchema(many=True))
    def get(self, args):
        """
        Query a suburb name by postcode value

        Returns a list of suburbs associated with the postcode value.

        #### Query Parameters
        - `suburb`: String, optional - The postcode value to query
        suburbs for.

        #### Responses
        - 200: Success - Returns a list of suburbs matching
        the query.
        - 400: Bad Request - If validation of the query parameters fails.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 500: Internal Server Error - If an unexpected error occurs during
        the query.
        """
        try:
            if 'postcode' in args:
                all_related_suburbs = fetch_suburbs_by_postcode(args)
            else:
                all_related_suburbs = []

            current_app.logger.info(
                f"Query successfully returned: {all_related_suburbs}")
            return all_related_suburbs
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}')
        except Exception as e:
            current_app.logger.error(
                f"Error occurred when querying suburbs by postcode: {e}")
            abort(500, message="Error: Failed to query suburbs by postcode. Please try again later.")
            
            
@bp.route('/<int:id>')
class SuburbsById(MethodView):
    @bp.response(200, SuburbSchema())
    def get(self, id):  # captured as a view arg
        """
        Get a suburb by Id

        Retrieves a suburb by its id from the database.

        ### Path Parameters
        - `id`: Integer, required - The ID of the suburb to retrieve.

        ### Responses
        - 200: Success - Returns the suburb with the specified ID.
        - 404: Not Found - If a suburb with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs during retrieval.
        """
        try:
            found_suburb = get_suburb_by_id(id)
            current_app.logger.info(f"Found suburb: {found_suburb}")
            return found_suburb
        except NotFoundException as e:
            current_app.logger.error(f"Suburb with id: {id} not found when sent to the service with e: {e}")
            abort(404, message=f'Suburb with id: {id} not found')
        except Exception as e:
            current_app.logger.error(f"Error in updating suburb with id {id}: {e}")
            abort(500, message="Failed to update a suburb")

    @token_required
    @bp.response(204)
    def delete(self, id):
        """
        Delete a suburb by Id (Protected)

        Deletes a suburb by Id. This endpoint is protected and requires Bearer Authentication.

        ### Path Parameters
        - `id`: Integer, required - The ID of the suburb to delete.

        ### Responses
        - 204: No Content - Successfully deleted the suburb.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 404: Not Found - If a suburb with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs during deletion.
        """
        try:
            delete_suburb_by_id(id)
            current_app.logger.info(f"suburb with {id} has been deleted")
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Suburb with id: {id} not found when trying to delete')
        except Exception as e:
            current_app.logger.error(f"Error in deleting suburb with id {id}: {e}")
            abort(500, message="Failed to delete a suburb")

    @token_required
    @bp.arguments(SuburbSchemaArgs)
    @bp.response(200, SuburbSchema())
    def patch(self, data, id):
        """
        Update a suburb by Id (Protected)

        Updates a suburb by Id. This endpoint is protected and requires Bearer Authentication.

        ### Request Body
        - `name`: String, optional
        - `state`: String, optional

        ### Path Parameters
        - `id`: Integer, required - The ID of the suburb to update.

        ### Responses
        - 200: Success - Returns the updated suburb.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 404: Not Found - If a suburb with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs during update.
        """
        try:
            updated_suburb = update_suburb_by_id(data, id)
            current_app.logger.info(f"Updated suburb: {updated_suburb}")
            return updated_suburb
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Suburb with id: {id} not found when trying to update')
        except Exception as e:
            current_app.logger.error(f"Error in updating suburb with id {id}: {e}")
            abort(500, message="Failed to update a suburb")
