from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.services.postcode_service import PostCodeService
from flask_smorest import Blueprint
from app.schemas.postcode_schema import PostCodeSchema
import logging # Task: review a better logging strategy in the config

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode_bp', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

postcode_service = PostCodeService()

# utilising fuctional-based approach so not using Methodview
'''GET ALL POSTCODES'''
@bp.route('/', methods=['GET'])
@bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi docs
def get_all_postcodes():
    all_postcodes = postcode_service.get_all_postcodes()
    logging.info(f"All postcodes successful sent with a count of {len(all_postcodes)} postcodes")
    return all_postcodes

'''CREATE'''
@bp.route('/', methods=['POST'])
@bp.response(201, PostCodeSchema()) # Flask-Smorest with Marshmallow takes care of serialize/deserialzing
def create_postcode(): 
    res_body = request.get_json()
    if not res_body:
        logging.error(f"No input data was provided at create for postcode")
        return jsonify({'message': 'No input data provided'}), 400
    
    schema = PostCodeSchema()
    
    # manually loading to add error handling
    try:
        data = schema.load(res_body) 
    except ValidationError as err:
        logging.error(f"There was an error mapping request to the postcode schema")
        return jsonify(err.messages), 422
    
    new_postcode = postcode_service.create_postcode(data)
    if not new_postcode:
        logging.error(f"Error in creating a new postcode")
        return jsonify({'message': 'Failed to create postcode'}), 400
    
    logging.info(f"Created postcode: {new_postcode}")
    return new_postcode

'''UPDATE'''
@bp.route('/<int:id>', methods=['PATCH'])
@bp.response(200, PostCodeSchema())
def get_postcode_by_id(id):
    res_body = request.get_json()
    if not res_body:
        logging.error(f"No input data was provided at updating postcode with id: {id}")
        return jsonify({'message': 'No input data provided'}), 400
    
    schema = PostCodeSchema()
    
    try:
        data = schema.load(res_body) 
    except ValidationError as err:
        logging.error(f"There was an error mapping request to the postcode schema")
        return jsonify(err.messages), 422
    
    updated_postcode = postcode_service.create_postcode(id, data)
    if not updated_postcode:
        logging.error(f"Error in updating postcode with id: {id} ")
        return jsonify({'message': 'Failed to create postcode'}), 400
    
    logging.info(f"Found postcode: {updated_postcode}")
    return updated_postcode

'''DELETE'''
# @bp.route('/<int:id>', methods=['DELETE'])
# @bp.response(200, PostCodeSchema())
# def get_postcode_by_id(id):
#     found_postcode = postcode_service.get_postcode_by_id(id)
#     if not found_postcode:
#         return jsonify({'message': 'Postcode not found'}), 404
#     print(f"Found postcode: {found_postcode}")
#     return found_postcode