import pytest

from app import create_app, db
from app.models.board_game import BoardGame
from app.models.collection import Collection
from app.models.review import Review
from config import config

from tests.db_test_data import insert_test_data


@pytest.fixture(scope="function")
def app():
    app_config = config["testing"]
    app = create_app(app_config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_test_data()
    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


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


@pytest.fixture()
def game():
    game = BoardGame(
        title="Wingspan",
        description="A card-driven, engine-building board game in which one to five players compete to attract birds to their wildlife reserves.",
        min_player_count=1,
        max_player_count=5,
        play_time_minutes=60,
        release_date="2020-09-17",
        age=12,
        weight=2.5,
        genre_id=1,
        designer_id=1,
        publisher_id=1,
        image_link="https://stonemaiergames.com/wp-content/uploads/2019/02/3d-wingspan-300x294.png",
    )


@pytest.fixture()
def search_results():
    return  # TODO


@pytest.fixture()
def search_results_no_search_term():
    return  # TODO


@pytest.fixture()
def reviews_for_user_1():
    return  # TODO


@pytest.fixture()
def collection_1_games():
    return  # TODO


@pytest.fixture()
def all_reviews_page_one():
    return  # TODO


@pytest.fixture()
def all_reviews_page_two():
    return  # TODO


@pytest.fixture()
def review_1():
    return  # TODO


@pytest.fixture()
def all_games_page_one():
    return  # TODO


@pytest.fixture()
def all_games_page_two():
    return  # TODO


@pytest.fixture()
def game_1():
    return  # TODO


@pytest.fixture()
def reviews_for_game_1():
    return  # TODO


@pytest.fixture()
def new_game_response():
    return  # TODO


@pytest.fixture()
def update_game_response():
    return  # TODO


@pytest.fixture()
def delete_game_response():
    return  # TODO


# =====================
#  Error responses
# =====================


@pytest.fixture()
def not_found_error():
    return {"success": False, "error": 404, "message": "Not found"}
