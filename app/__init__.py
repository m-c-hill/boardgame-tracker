from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()

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

    # from app.offers import bp as users_bp

    # app.register_blueprint(users_bp, url_prefix="/api")

    return app