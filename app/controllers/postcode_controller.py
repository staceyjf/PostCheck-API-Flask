from flask import jsonify, request
from app.services.postcode_service import PostCodeService
from flask_smorest import Blueprint
from app.schemas.postcode_schema import PostCodeSchema

# blueprint adds to the factory function / making it reusable
bp = Blueprint('postcode_bp', __name__, url_prefix='/postcode', description="Operations on postcodes")

postcode_service = PostCodeService()

@bp.route('/', methods=['GET'])
@bp.response(200, PostCodeSchema(many=True))  # smorest add for openApi
def get_all_postcodes():
    """Get a list of all postcodes"""
    print("All postcodes successful sent")
    return postcode_service.get_all_postcodes()