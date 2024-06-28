from app.extensions import db
from app.models.models import User
from sqlalchemy.orm import joinedload

def repo_get_all_users():
    return User.query.order_by(User.username).all()

def repo_find_user_by_username(supplied_username):
    return User.query.filter(username = supplied_username).first()