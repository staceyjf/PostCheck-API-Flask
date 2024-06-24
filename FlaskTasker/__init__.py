from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()
cors = CORS()

## import the entities
from .models import Todo, Colour, db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/todo_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    @app.route('/')
    def hello_world():
        return 'Hello, there World!'

    return app