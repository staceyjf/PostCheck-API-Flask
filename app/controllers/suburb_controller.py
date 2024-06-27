from flask import current_app
from flask.views import MethodView
from marshmallow import ValidationError
from app.services.suburb_Service import get_all_suburbs, get_suburb_by_id, create_suburb,update_suburb_by_id, delete_suburb_by_id
from flask_smorest import Blueprint, abort
from app.schemas.suburb_schema import SuburbSchema
from app.schemas.suburb_schema_args import SuburbSchemaArgs
from app.exceptions.CustomErrors import NotFoundException, ValidationError

# blueprint adds to the factory function / making it reusable
bp = Blueprint('suburb', __name__, url_prefix='/api/v1/suburbs/', description="Operations on suburbs")

@bp.route('/')
class Suburbs(MethodView):
    @bp.response(200, SuburbSchema(many=True))  # smorest add for openApi docs
    def get(self):
        """Fetch all suburbs

        Retrieves a list of all suburbs from the database.
        """
        all_suburbs = get_all_suburbs()
        current_app.logger.info(f"All suburbs successful sent with a count of {len(all_suburbs)} suburbs")
        return all_suburbs
    
    @bp.arguments(SuburbSchemaArgs) # Parse and validates the request body
    @bp.response(201, SuburbSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
    def post(self, data):
        """Create a new suburb
        
        Creates a new suburb with the provided data.
        """
        try:
            new_suburb = create_suburb(data)
            current_app.logger.info(f"Created suburb: {new_suburb}")
            return new_suburb
        except NotFoundException as e:
            current_app.logger.error(f"Issue with a Suburb Id: {e}")
            abort(404, message=f'Issue with a Suburb Id')
        except Exception as e:
            current_app.logger.error(f"Error in creating a new suburb: {e}")
            abort(500, message="Failed to create suburb")  

        
@bp.route('/<int:id>')
class SuburbsById(MethodView):
    @bp.response(200, SuburbSchema()) 
    def get(self,id): #captured as a view arg
        """Get a suburb by Id
        
        Retrieves a suburb by its id from the database.
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
            
    @bp.response(204)
    def delete(self,id):
        """DELETE a suburb by Id
                
        Deletes a suburb by Id.
        """
        try: 
            delete_suburb_by_id(id)  
            current_app.logger.info(f"suburb with {id} has been delete.")
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Suburb with id: {id} not found when trying to delete')    

    @bp.arguments(SuburbSchemaArgs) 
    @bp.response(200, SuburbSchema())
    def patch(self, data, id):
        """Update a suburb by Id
                
        Updates a suburb by Id.
        """
        try:
            updated_suburb = update_suburb_by_id(data, id)
            current_app.logger.info(f"Updated suburb: {updated_suburb}")
            return updated_suburb
        except NotFoundException as e:
            current_app.logger.error(f"Error: {e}")
            abort(404, message=f'Suburb with id: {id} not found when trying to update')  