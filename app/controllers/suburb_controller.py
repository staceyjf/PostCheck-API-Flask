from flask import request, jsonify
from marshmallow import ValidationError
from app.services.suburb_Service import get_all_suburbs, get_suburb_by_id, create_suburb
from flask_smorest import Blueprint
from app.schemas.suburb_schema import SuburbSchema
import logging # Task: review a better logging strategy in the config

# blueprint adds to the factory function / making it reusable
bp = Blueprint('suburb_bp', __name__, url_prefix='/api/v1/suburbs', description="Operations on suburbs")

# utilising fuctional-based approach so not using Methodview
'''READ'''
@bp.route('/', methods=['GET'])
@bp.response(200, SuburbSchema(many=True))  # smorest add for openApi docs
def fetch_all_suburbs():
    all_suburbs = get_all_suburbs()
    logging.info(f"All suburbs successful sent with a count of {len(all_suburbs)} suburbs")
    return all_suburbs