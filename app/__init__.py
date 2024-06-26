from config import Config
from flask import Flask, jsonify
from app.controllers.postcode_controller import bp as postcode_controller
from app.controllers.suburb_controller import bp as suburb_controller
from app.extensions import db, api, cors,migrate
import app.models
from logging.config import dictConfig

def create_app():
    # configure builtin Logging using Flask example
    # TASK: Look into FileHandler and other configs for my needs
    dictConfig({
        'version': 1,
        'formatters': {'all_info_logger': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }}, 
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'all_info_logger'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

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