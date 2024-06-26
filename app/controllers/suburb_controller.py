from flask import request, jsonify, current_app
from marshmallow import ValidationError
from app.services.suburb_Service import get_all_suburbs, get_suburb_by_id, create_suburb
from flask_smorest import Blueprint
from app.schemas.suburb_schema import SuburbSchema

# blueprint adds to the factory function / making it reusable
bp = Blueprint('suburb_bp', __name__, url_prefix='/api/v1/suburbs', description="Operations on suburbs")

# utilising fuctional-based approach so not using Methodview
'''READ'''
@bp.route('/', methods=['GET'])
@bp.response(200, SuburbSchema(many=True))  # smorest add for openApi docs
def fetch_all_suburbs():
    all_suburbs = get_all_suburbs()
    current_app.logger.info(f"All suburbs successful sent with a count of {len(all_suburbs)} suburbs")
    return all_suburbs

@bp.route('/<int:id>', methods=['GET'])
@bp.response(200, SuburbSchema()) 
def fetch_suburb_by_id(id): #captured as a view arg 
    found_suburb = get_suburb_by_id(id)
    if not found_suburb:
        current_app.logger.error(f"Suburb with id: {id} not found when sent to the service")
        return jsonify({'message': f'Suburb with id: {id} not found'}), 404
    current_app.logger.info(f"Found suburb: {found_suburb}")
    return found_suburb

'''CREATE'''
@bp.route('/', methods=['POST'])
@bp.response(201, SuburbSchema())  # Flask-Smorest with Marshmallow takes care of serialize/deserializing
def create_new_suburb():
    req_body = request.get_json()
    if not req_body:
        current_app.logger.error("No input data was provided at create for suburb")
        return jsonify({'message': 'No input data provided'}), 400

    schema = SuburbSchema()

    # Manually loading to add error handling
    try:
        data = schema.load(req_body)
    except ValidationError as e:
        current_app.logger.error("There was an error mapping request to the suburb schema")
        return jsonify(e.messages), 422

    # handle any errors raised in the service level
    try:
        new_suburb = create_suburb(data)
    except ValueError as e:
        current_app.logger.error(f"Validation error: {e}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error in creating a new suburb: {e}")
        return jsonify({'message': 'Failed to create suburb'}), 500

    current_app.logger.info(f"Created suburb: {new_suburb}")
    return new_suburb