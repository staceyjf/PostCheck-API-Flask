from flask import request, jsonify
from marshmallow import ValidationError
from app.services.postcode_service import get_all_postcodes, create_postcode
from flask_smorest import Blueprint
from app.schemas.postcode_schema import PostCodeSchema
import logging # Task: review a better logging strategy in the config

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode_bp', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

# utilising fuctional-based approach so not using Methodview
'''READ'''
@bp.route('/', methods=['GET'])
@bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi docs
def fetch_all_postcodes():
    all_postcodes = get_all_postcodes()
    logging.info(f"All postcodes successful sent with a count of {len(all_postcodes)} postcodes")
    return all_postcodes

#TASK: add get by id

'''CREATE'''
@bp.route('/', methods=['POST'])
@bp.response(201, PostCodeSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
def create_new_postcode():
    req_body = request.get_json()
    if not req_body:
        logging.error("No input data was provided at create for postcode")
        return jsonify({'message': 'No input data provided'}), 400

    schema = PostCodeSchema()

    # Manually loading to add error handling
    try:
        data = schema.load(req_body)
    except ValidationError as err:
        logging.error("There was an error mapping request to the postcode schema")
        return jsonify(err.messages), 422

    # handle any errors raised in the service level
    try:
        new_postcode = create_postcode(data)
    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        logging.error(f"Error in creating a new postcode: {e}")
        return jsonify({'message': 'Failed to create postcode'}), 500

    logging.info(f"Created postcode: {new_postcode}")
    return jsonify(new_postcode), 201

# '''UPDATE'''
# @bp.route('/<int:id>', methods=['PATCH'])
# @bp.response(200, PostCodeSchema())
# def get_postcode_by_id(id):
#     res_body = request.get_json()
#     if not res_body:
#         logging.error(f"No input data was provided at updating postcode with id: {id}")
#         return jsonify({'message': 'No input data provided'}), 400
    
#     schema = PostCodeSchema()
    
#     try:
#         data = schema.load(res_body) 
#     except ValidationError as err:
#         logging.error(f"There was an error mapping request to the postcode schema")
#         return jsonify(err.messages), 422
    
#     updated_postcode = update_postcode(id, data)
#     if not updated_postcode:
#         logging.error(f"Error in updating postcode with id: {id} ")
#         return jsonify({'message': 'Failed to create postcode'}), 400
    
#     logging.info(f"Found postcode: {updated_postcode}")
#     return updated_postcode

'''DELETE'''
# @bp.route('/<int:id>', methods=['DELETE'])
# @bp.response(200, PostCodeSchema())
# def get_postcode_by_id(id):
#     found_postcode = get_postcode_by_id(id)
#     if not found_postcode:
#         return jsonify({'message': 'Postcode not found'}), 404
#     print(f"Found postcode: {found_postcode}")
#     return found_postcode