from os import environ as env

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Import models
from app.models.board_game import BoardGame, Designer, Genre, Publisher
from app.models.user import User
from app.models.review import Review


def create_app(config_class: Config):
    """
    Application factory to create a Flask app with the supplied configuration
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = env.get("APP_SECRET_KEY")

    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate.init_app(app, db, compare_type=True)
        oauth.init_app(app)

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

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
