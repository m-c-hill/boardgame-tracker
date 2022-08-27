import os

import pytest

from app import create_app

from app.models.collection import Collection
from app.models.review import Review

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


# =======================
#  Model fixtures
# =======================

@pytest.fixture()
def collection():
    return Collection(user_id=1)

@pytest.fixture()
def game_id():
    return 1

@pytest.fixture
def user_id():
    return 1

@pytest.fixture
def review():
    return Review(
        game_id=1,
        review_text="",
        rating=5,
        user_id=1,
    )
