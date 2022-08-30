import os


def get_database_path(database_name):
    postgres_user = os.environ.get("POSTGRES_USER", "postgres")
    postgres_pw = os.environ.get("POSTGRES_PW", "password")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    return f"postgresql://{postgres_user}:{postgres_pw}@{host}:5432/{database_name}"


class Config(object):
    """
    Set the config variables for the Flask app
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    database_name = "boardgames"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or get_database_path(
        "boardgames_dev"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or get_database_path(
        "boardgames_test"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or get_database_path(
        "boardgames"
    )


class HerokuConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or get_database_path(
    #     "boardgames"
    # )

class DockerConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_database_path(
        "boardgames"
    )

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}
