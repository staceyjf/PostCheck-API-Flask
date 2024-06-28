from flask import current_app
from flask.views import MethodView
from app.services.postcode_service import get_all_postcodes, create_postcode, get_postcode_by_id, delete_postcode_by_id, update_postcode_by_id, fetch_postcodes_by_suburb, fetch_relatedSuburbs_by_postcode
from flask_smorest import Blueprint, abort
from app.schemas.postcode_schema import PostCodeSchema
from app.schemas.postcode_schema_args import PostCodeSchemaArgs, PostCodeSchemaBySuburbName
from app.exceptions.CustomErrors import NotFoundException, CustomValidationError

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

# using a class based approach as recommended by smorest to utilise swagger 
@bp.route('/')
class Postcodes(MethodView):
    @bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi docs
    def get(self):
        """Fetch all postcodes

        Retrieves a list of all postcodes from the database.
        """
        all_postcodes = get_all_postcodes()
        current_app.logger.info(f"All postcodes successful sent with a count of {len(all_postcodes)} postcodes")
        return all_postcodes
    
    @bp.arguments(PostCodeSchemaArgs) # Parse and validates the request body
    @bp.response(201, PostCodeSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
    def post(self, data):
        """Create a new postcode
        
        Creates a new postcode with the provided data.
        """
        try:
            new_postcode = create_postcode(data)
            current_app.logger.info(f"Created postcode: {new_postcode}")
            return new_postcode
        except CustomValidationError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}')
        except NotFoundException as e:
            current_app.logger.error(f"Issue with a Suburb Id: {e}")
            abort(404, message=f'Issue with a Suburb Id')     
        except Exception as e:
            current_app.logger.error(f"Error in creating a new postcode: {e}")
            abort(500, message="Failed to create postcode")
            
@bp.route('/query')
class PostcodesQueries(MethodView):            
    @bp.arguments(PostCodeSchemaBySuburbName, location="query") 
    @bp.response(200, PostCodeSchema(many=True)) 
    def get(self, args):
        """Query a postcode by suburb name or postcode value
        
        Returns a list of postcodes associated with the suburb name or postcode value
        """
        try:
            if 'suburb' in args:
                all_related_postcodes = fetch_postcodes_by_suburb(args)
            elif 'postcode' in args:
                all_related_postcodes = fetch_relatedSuburbs_by_postcode(args)
            else:
                all_related_postcodes = []
                
            current_app.logger.info(f"Created postcode: {all_related_postcodes}")
            return all_related_postcodes
        except CustomValidationError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}')
        except NotFoundException as e:
            current_app.logger.error(f"Resource not found: {e}")
            abort(404, message=f'Resource not found')     
        except Exception as e:
            current_app.logger.error(f"Error occurred when querying postcodes by suburb: {e}")
            abort(500, message="Failed to query postcodes by suburb")
        
@bp.route('/<int:id>')
class PostCodeById(MethodView):
    @bp.response(200, PostCodeSchema())
    def get(self,id):
        """Get a postcode by Id
            
        Retrieves a postcode by its id from the database.
        """
        try: 
            found_postcode = get_postcode_by_id(id)  
            current_app.logger.info(f"Found postcode: {found_postcode}")
            return found_postcode
        except NotFoundException as e:
            current_app.logger.error(f"Postcode with id: {id} not found when sent to the service with e: {e}")
            abort(404, message=f'Postcode with id: {id} not found')
        except Exception as e:
            current_app.logger.error(f"Error in updating postcode with id {id}: {e}")
            abort(500, message="Failed to update a postcode")
            
    @bp.response(204)
    def delete(self,id):
        """DELETE a postcode by Id
                
        Deletes a postcode by Id.
        """
        try: 
            delete_postcode_by_id(id)  
            current_app.logger.info(f"Postcode with {id} has been delete.")
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Postcode with id: {id} not found when trying to delete')    

    @bp.arguments(PostCodeSchemaArgs) 
    @bp.response(200, PostCodeSchema())
    def patch(self, data, id):
        """Update a postcode by Id
                
        Updates a postcode by Id.
        """
        try:
            updated_postcode = update_postcode_by_id(data, id)
            current_app.logger.info(f"Updated postcode: {updated_postcode}")
            return updated_postcode
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Postcode with id: {id} not found when trying to update')
        
        
        

