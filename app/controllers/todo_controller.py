from flask import jsonify, request
from app.services.todo_service import TodoService
from flask_smorest import Blueprint
from app.schemas.todo_schema import TodoSchema

# blueprint adds to the factory function / making it reusable
bp = Blueprint('todo_bp', __name__, url_prefix='/todos', description="Operations on todos")

todo_service = TodoService()

@bp.route('/', methods=['GET'])
@bp.response(200, TodoSchema(many=True))  # smorest add for openApi
def get_todos():
    """Get a list of all todos"""
    print("All todo successful sent")
    return todo_service.get_all_todos()