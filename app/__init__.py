from config import Config
from flask import Flask, jsonify
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

    return app