import os
from os import environ as env

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

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


from app.config import config

# Import models
from app.domain.board_game import BoardGame, Designer, Genre, Publisher
from app.domain.collection import Collection
from app.domain.review import Review
from app.domain.user import User


def create_app(config_name: str = os.getenv("FLASK_CONFIG") or "default"):
    """
    Application factory to create a Flask app with the supplied configuration
    """
    app = Flask(__name__)
    config_class = config[config_name]
    app.config.from_object(config_class)
    app.secret_key = env.get("APP_SECRET_KEY")

    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate.init_app(app, db, compare_type=True)
        oauth.init_app(app)

        from .main.errors import register_error_handlers

        register_error_handlers(app)

        # TODO: temporary to seed database with initial data. Remove in future.
        try:
            from tests.db_test_data import insert_test_data

            insert_test_data()
        except:
            pass

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/api")

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .swagger import swaggerui_blueprint

    app.register_blueprint(swaggerui_blueprint)

    return app
