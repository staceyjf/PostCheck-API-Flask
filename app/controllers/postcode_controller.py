from flask import current_app
from flask.views import MethodView
from app.services.postcode_service import (
    get_all_postcodes, create_postcode, get_postcode_by_id,
    delete_postcode_by_id, update_postcode_by_id,
    fetch_postcodes_by_suburb, fetch_relatedSuburbs_by_postcode
)
from flask_smorest import Blueprint, abort
from app.schemas.postcode_schema import PostCodeSchema
from app.schemas.postcode_schema_args import (
    PostCodeSchemaArgs, PostCodeSchemaBySuburbName
)
from app.exceptions.CustomExceptions import (
    NotFoundException, ServiceException, DbValidationError)
from app.auth.token_required_decorator import token_required

# defining blueprint to aid in modularization
bp = Blueprint('postcode', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")


# using a class based approach
# as recommended by smorest to utilise swagger
@bp.route('/')
class Postcodes(MethodView):
    @bp.response(200, PostCodeSchema(many=True))
    def get(self):
        """
        Fetch all postcodes

        Retrieves a list of all postcodes from the database.

        #### Responses
        - 200: Success - Returns a list of all postcodes.
        """
        all_postcodes = get_all_postcodes()
        current_app.logger.info(f"All postcodes successfully sent with a count of {len(all_postcodes)} postcodes")
        return all_postcodes

    @token_required
    @bp.arguments(PostCodeSchemaArgs)  # Parse and validates the request body
    @bp.response(201, PostCodeSchema())
    # Flask-Smorest with Marshmallow takes care of serialize/deserializing
    def post(self, data):
        """
        Create a new postcode (Protected)

        Creates a new postcode with the provided data.

        #### Request Body
        - `suburbIds`: Integer, optional -
        The IDs of the suburbs associated with the postcode.
        - `postcode`: String, required - The postcode value.

        #### Responses
        - 201: Success - Returns the newly created postcode.
        - 400: Bad Request - If validation of the request body fails.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 500: Internal Server Error - If an unexpected error occurs during
        postcode creation.
        """
        try:
            new_postcode = create_postcode(data)
            current_app.logger.info(f"Created postcode: {new_postcode}")
            return new_postcode
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'{e}')
        except NotFoundException as e:
            current_app.logger.error(f"Issue with a Suburb Id: {e}")
            abort(400, message=f'Issue when trying to add Suburb Id')
        except DbValidationError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'{e}')
        except Exception as e:
            current_app.logger.error(f"Error in creating a new postcode: {e}")
            abort(500, message="Error: Failed to query postcodes by suburb. Please try again later.")


@bp.route('/query')
class PostcodesQueries(MethodView):
    @bp.arguments(PostCodeSchemaBySuburbName, location="query")
    @bp.response(200, PostCodeSchema(many=True))
    def get(self, args):
        """
        Query a postcode by suburb name or postcode value

        Returns a list of postcodes associated with the suburb name or
        postcode value.

        #### Query Parameters
        - `suburb`: String, optional - The name of the suburb to query
        postcodes for.
        - `postcode`: String, optional - The postcode value to query
        suburbs for.

        #### Responses
        - 200: Success - Returns a list of postcodes or suburbs matching
        the query.
        - 400: Bad Request - If validation of the query parameters fails.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 500: Internal Server Error - If an unexpected error occurs during
        the query.
        """
        try:
            if 'suburb' in args:
                all_related_postcodes = fetch_postcodes_by_suburb(args)
            elif 'postcode' in args:
                all_related_postcodes = fetch_relatedSuburbs_by_postcode(args)
            else:
                all_related_postcodes = []

            current_app.logger.info(
                f"Query successfully returned: {all_related_postcodes}")
            return all_related_postcodes
        except ServiceException as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}')
        except Exception as e:
            current_app.logger.error(
                f"Error occurred when querying postcodes by suburb: {e}")
            abort(500, message="Error: Failed to query postcodes by suburb. Please try again later.")


@bp.route('/<int:id>')
class PostCodeById(MethodView):
    @bp.response(200, PostCodeSchema())
    def get(self, id):
        """
        Get a postcode by ID

        Retrieves a postcode by its ID from the database.

        #### Path Parameters
        - `id`: Integer, required - The ID of the postcode to retrieve.

        #### Responses
        - 200: Success - Returns the postcode with the specified ID.
        - 404: Not Found - If a postcode with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs during
        retrieval.
        """
        try:
            found_postcode = get_postcode_by_id(id)
            current_app.logger.info(f"Found postcode: {found_postcode}")
            return found_postcode
        except NotFoundException as e:
            current_app.logger.error(f"Postcode with id: {id} not found when sent to the service with e: {e}")
            abort(404, message=f'Postcode with id: {id} not found')
        except Exception as e:
            current_app.logger.error(
                f"Error in updating postcode with id {id}: {e}")
            abort(500, message="Failed to update a postcode")

    @token_required
    @bp.response(204)
    def delete(self, id):
        """
        Delete a postcode by ID (Protected)

        Deletes a postcode by its ID.

        #### Path Parameters
        - `id`: Integer, required - The ID of the postcode to delete.

        #### Responses
        - 204: No Content - Successfully deleted the postcode.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 404: Not Found - If a postcode with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs during
        deletion.
        """
        try:
            delete_postcode_by_id(id)
            current_app.logger.info(f"Postcode with {id} has been deleted")
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Postcode with id: {id} not found when trying to delete')
        except Exception as e:
            current_app.logger.error(f"Error in deleting postcode with id {id}: {e}")
            abort(500, message="Failed to delete a postcode")

    @token_required
    @bp.arguments(PostCodeSchemaArgs)
    @bp.response(200, PostCodeSchema())
    def patch(self, data, id):
        """
        Update a postcode by ID (Protected)

        Updates a postcode by its ID with the provided data.

        #### Request Body
        - `suburb_id`: Integer, optional - The new ID of the suburb associated
        with the postcode.
        - `postcode`: String, optional - The new postcode value.

        #### Path Parameters
        - `id`: Integer, required - The ID of the postcode to update.

        #### Responses
        - 200: Success - Returns the updated postcode.
        - 401: Unauthorized - If the authentication token is missing or invalid.
        - 404: Not Found - If a postcode with the specified ID does not exist.
        - 500: Internal Server Error - If an unexpected error occurs
        during update.
        """
        try:
            updated_postcode = update_postcode_by_id(data, id)
            current_app.logger.info(f"Updated postcode: {updated_postcode}")
            return updated_postcode
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Postcode with id: {id} not found when trying to update')
        except Exception as e:
            current_app.logger.error(
                f"Error in updating postcode with id {id}: {e}")
            abort(500, message="Failed to update a postcode")