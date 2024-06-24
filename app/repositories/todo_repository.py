from sqlalchemy import select
from app.extensions import db
from app.models.todo_model import Todo
from app.models.colour_model import Colour

class TodoRepository:
    def get_all_todos(self):
        return Todo.query.all()