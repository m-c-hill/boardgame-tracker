import os

import pytest

from app import create_app


# TODO: set up testing client and app
@pytest.fixture()
def client():
    app = create_app()
    postgres_user = os.environ.get("POSTGRES_USER", "postgres")
    postgres_pw = os.environ.get("POSTGRES_PW", "password")
    test_database_name = "trivia_test"
    test_database_path = (
        f"postgres://{postgres_user}:{postgres_pw}@localhost:5432/{test_database_name}"
    )
    # db = setup_db(app, test_database_path)
    # db.drop_all()
    # db.create_all()
    # insert_dummy_data()  # Populate database with test data
    yield app.test_client()
    # db.drop_all()
