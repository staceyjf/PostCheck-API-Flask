from app.extensions import db
from app.models.models import User
import uuid
from werkzeug.security import generate_password_hash


def repo_get_all_users():
    return User.query.order_by(User.username).all()


def repo_find_user_by_username(supplied_username):
    return User.query.filter_by(username=supplied_username).first()


def repo_create_user(data):
    generated_public_id = str(uuid.uuid4())  # generates a str of a random UUID based on random numbers.
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        public_id=generated_public_id,
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user
