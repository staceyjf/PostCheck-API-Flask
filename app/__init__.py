from config import DevelopmentConfig
from flask import Flask, request, Response
from app.controllers.postcode_controller import bp as postcode_bp
from app.controllers.suburb_controller import bp as suburb_bp
from app.controllers.user_controller import bp as user_bp
from app.controllers.report_controller import bp as reporting_bp
from app.extensions import db, migrate
from logging.config import dictConfig
from flask_smorest import Api
from flask_cors import CORS


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

    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    # cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # api.init_app(app) didn't seem to work
    api = Api(app)

    api.register_blueprint(postcode_bp)
    api.register_blueprint(suburb_bp)
    api.register_blueprint(user_bp)
    api.register_blueprint(reporting_bp)

    # hack to overcome the cors issue
    @app.before_request
    def basic_authentication():
        if request.method.lower() == 'options':
            return Response()

    return app
