from config import Config
from flask import Flask, jsonify
from app.controllers.postcode_controller import bp as postcode_controller
from app.controllers.suburb_controller import bp as suburb_controller
from app.extensions import db, api, cors,migrate

## import the entities and database instance
import app.models

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    cors.init_app(app)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    app.register_blueprint(postcode_controller)
    app.register_blueprint(suburb_controller)

    return app