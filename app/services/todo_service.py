from app.models.todo_model import Todo
from app.repositories.todo_repository import TodoRepository

todo_repository = TodoRepository()

class TodoService:
    def get_all_todos(self):
        return todo_repository.get_all_todos()