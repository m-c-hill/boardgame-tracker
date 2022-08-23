from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()

from app.models.models import BoardGame, Genre, Designer, Publisher, Review, User


def create_app(config_class: Config):
    """
    Application factory to create a Flask app with the supplied configuration
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate.init_app(app, db, compare_type=True)

    @app.after_request
    def after_request(response):
        """
        When a request is received, run this method to add additional CORS headers to the response.
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/api")

    return app
