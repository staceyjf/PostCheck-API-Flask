from flask import request, jsonify
from marshmallow import ValidationError
from app.services.suburb_Service import PostCodeService
from flask_smorest import Blueprint
from app.schemas.postcode_schema import PostCodeSchema
import logging # Task: review a better logging strategy in the config

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode_bp', __name__, url_prefix='/api/v1/postcodes', description="Operations on postcodes")

# utilising fuctional-based approach so not using Methodview
'''READ'''
@bp.route('/', methods=['GET'])
@bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi docs
def get_all_postcodes():
    all_postcodes = postcode_service.get_all_postcodes()
    logging.info(f"All postcodes successful sent with a count of {len(all_postcodes)} postcodes")
    return all_postcodes