from flask import request, jsonify, current_app
from flask.views import MethodView
from marshmallow import ValidationError
from app.services.postcode_service import get_all_postcodes, create_postcode, get_postcode_by_id
from flask_smorest import Blueprint, abort
from app.schemas.postcode_schema import PostCodeSchema

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

# utilising fuctional-based approach so not using Methodview
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
    
    @bp.arguments(PostCodeSchema) # Parse and validates the request body
    @bp.response(201, PostCodeSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
    def post(self, data):
        # handle any errors raised in the service level
        """Create a new postcode
        
        Creates a new postcode with the provided data.
        """
        try:
            new_postcode = create_postcode(data)
        except ValueError as e:
            current_app.logger.error(f"Validation error: {e}")
            abort(400, message=f'Validation error: {e}') 
        except Exception as e:
            current_app.logger.error(f"Error in creating a new postcode: {e}")
            abort(500, message="Failed to create postcode") 

        current_app.logger.info(f"Created postcode: {new_postcode}")
        return new_postcode, 201

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
        except ValueError as e:
            current_app.logger.error(f"Postcode with id: {id} not found when sent to the service with e: {e}")
            abort(404, message=f'Postcode with id: {id} not found')  



# '''UPDATE'''
# @bp.route('/<int:id>', methods=['PATCH'])
# @bp.response(200, PostCodeSchema())
# def get_postcode_by_id(id):
#     res_body = request.get_json()
#     if not res_body:
#         current_app.logger.error(f"No input data was provided at updating postcode with id: {id}")
#         return jsonify({'message': 'No input data provided'}), 400
    
#     schema = PostCodeSchema()
    
#     try:
#         data = schema.load(res_body) 
#     except ValidationError as err:
#         current_app.logger.error(f"There was an error mapping request to the postcode schema")
#         return jsonify(err.messages), 422
    
#     updated_postcode = update_postcode(id, data)
#     if not updated_postcode:
#         current_app.logger.error(f"Error in updating postcode with id: {id} ")
#         return jsonify({'message': 'Failed to create postcode'}), 400
    
#     current_app.logger.info(f"Found postcode: {updated_postcode}")
#     return updated_postcode

'''DELETE'''
