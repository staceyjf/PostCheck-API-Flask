from flask import request, jsonify, current_app
from marshmallow import ValidationError
from app.services.postcode_service import get_all_postcodes, create_postcode, get_postcode_by_id
from flask_smorest import Blueprint
from app.schemas.postcode_schema import PostCodeSchema

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode_bp', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

# utilising fuctional-based approach so not using Methodview
'''READ'''
@bp.route('/', methods=['GET'])
@bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi docs
def fetch_all_postcodes():
    all_postcodes = get_all_postcodes()
    current_app.logger.info(f"All postcodes successful sent with a count of {len(all_postcodes)} postcodes")
    return all_postcodes

@bp.route('/<int:id>', methods=['GET'])
@bp.response(200, PostCodeSchema())
def fetch_postcode_by_id(id):
    found_postcode = get_postcode_by_id(id)
    if not found_postcode:
        current_app.logger.error(f"Postcode with id: {id} not found when sent to the service")
        return jsonify({'message': f'Postcode with id: {id} not found'}), 404    
    current_app.logger.info(f"Found postcode: {found_postcode}")
    return found_postcode

'''CREATE'''
@bp.route('/', methods=['POST'])
@bp.response(201, PostCodeSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
def create_new_postcode():
    req_body = request.get_json()
    if not req_body:
        current_app.logger.error("No input data was provided at create for postcode")
        return jsonify({'message': 'No input data provided'}), 400

    schema = PostCodeSchema()

    # Manually loading to add error handling
    try:
        data = schema.load(req_body)   # remember this is a dict
    except ValidationError as e:
        current_app.logger.error("There was an error mapping request to the postcode schema")
        return jsonify(e.messages), 422

    # handle any errors raised in the service level
    try:
        new_postcode = create_postcode(data)
    except ValueError as e:
        current_app.logger.error(f"Validation error: {e}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in creating a new postcode: {e}")
        return jsonify({'message': 'Failed to create postcode'}), 500

    current_app.logger.info(f"Created postcode: {new_postcode}")
    return new_postcode, 201

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
