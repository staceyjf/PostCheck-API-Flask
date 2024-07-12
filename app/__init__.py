from config import ProductionConfig
from flask import Flask
from app.controllers.postcode_controller import bp as postcode_bp
from app.controllers.suburb_controller import bp as suburb_bp
from app.controllers.user_controller import bp as user_bp
from app.controllers.report_controller import bp as reporting_bp
from app.extensions import db, migrate
from logging.config import dictConfig
from flask_smorest import Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    # Configured builtin logging via Flask doc example
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
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(ProductionConfig)
    db.init_app(app)  # Set up SQLAclhemcy
    migrate.init_app(app, db)  # Set up Flask Migrate

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    api = Api(app)  # Set up smorest

    # Register app's blueprints which aid modularization
    # easy to add more functionality
    api.register_blueprint(postcode_bp)
    api.register_blueprint(suburb_bp)
    api.register_blueprint(user_bp)
    api.register_blueprint(reporting_bp)

    return app
