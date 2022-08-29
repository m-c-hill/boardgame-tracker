import pytest

from app import create_app, db
from app.models.board_game import BoardGame
from app.models.collection import Collection
from app.models.review import Review
from config import config
from tests.db_test_data import insert_test_data


# =======================
#  Test app and client
# =======================


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
    return BoardGame(
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


# =======================
#  Response fixtures
# =======================


@pytest.fixture()
def search_results():
    return {
        "games": [
            {
                "age": 10,
                "description": "Attract a beautiful and diverse collection of birds to your aviary.",
                "designer": 6,
                "genre": 1,
                "id": 1,
                "image_link": "https://boardgamegeek.com/image/4458123/wingspan",
                "max_player_count": 5,
                "min_player_count": 1,
                "play_time_minutes": 50,
                "publisher": 6,
                "release_date": "2019-09-01",
                "title": "Wingspan",
                "weight": 2.55,
            }
        ],
        "search_term": "wingspan",
        "success": True,
        "total_games": 1,
    }


@pytest.fixture()
def reviews_for_user_1():
    return {
        "reviews": [
            {
                "game_id": 1,
                "id": 1,
                "rating": 5,
                "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "user": 1,
            },
            {
                "game_id": 2,
                "id": 2,
                "rating": 4,
                "review_text": "Lectus vestibulum mattis ullamcorper velit sed ullamcorper.",
                "user": 1,
            },
            {
                "game_id": 3,
                "id": 3,
                "rating": 3,
                "review_text": "Vivamus at augue eget arcu. Quam pellentesque nec nam aliquam sem et tortor.",
                "user": 1,
            },
            {
                "game_id": 4,
                "id": 4,
                "rating": 4,
                "review_text": "Massa sapien faucibus et molestie ac feugiat. Risus in hendrerit gravida rutrum quisque non tellus orci ac.",
                "user": 1,
            },
        ],
        "success": True,
        "total_reviews_by_user": 4,
        "user_id": "630638af7fea339f9931f90c",
        "username": "admin",
    }


@pytest.fixture()
def collection_1_games():
    return {
        "success": True,
        "collection": {
            "id": 1,
            "user_id": 1,
            "games": [
                {
                    "id": 1,
                    "title": "Wingspan",
                    "description": "Attract a beautiful and diverse collection of birds to your aviary.",
                    "min_player_count": 1,
                    "max_player_count": 5,
                    "play_time_minutes": 50,
                    "release_date": "2019-09-01",
                    "age": 10,
                    "weight": 2.55,
                    "genre": 1,
                    "designer": 6,
                    "publisher": 6,
                    "image_link": "https://boardgamegeek.com/image/4458123/wingspan",
                },
                {
                    "id": 2,
                    "title": "7 Wonders Duel",
                    "description": "Science? Military? What will you draft to win this head-to-head version of 7 Wonders?",
                    "min_player_count": 2,
                    "max_player_count": 2,
                    "play_time_minutes": 30,
                    "release_date": "2018-01-01",
                    "age": 10,
                    "weight": 2.22,
                    "genre": 1,
                    "designer": 5,
                    "publisher": 5,
                    "image_link": "https://cf.geekdo-images.com/zdagMskTF7wJBPjX74XsRw__itemrep/img/x5L93n_pSsxfFZ0Ir-JqtjLf-Jw=/fit-in/246x300/filters:strip_icc()/pic2576399.jpg",
                },
                {
                    "id": 3,
                    "title": "Parks",
                    "description": "Hike through National Parks tiles, collecting memories and admiring gorgeous scenery.",
                    "min_player_count": 1,
                    "max_player_count": 5,
                    "play_time_minutes": 40,
                    "release_date": "2019-01-01",
                    "age": 10,
                    "weight": 2.16,
                    "genre": 3,
                    "designer": 4,
                    "publisher": 4,
                    "image_link": "https://cf.geekdo-images.com/mF2cSNRk2O6HtE45Sl9TcA__opengraph/img/uoYOX2JqGtmeJ6o5wMmfypahWEs=/fit-in/1200x630/filters:strip_icc()/pic4852372.jpg",
                },
            ],
            "private": True,
        },
        "total_games": 3,
    }


@pytest.fixture()
def all_reviews_page_one():
    return {
        "reviews": [
            {
                "game_id": 1,
                "id": 1,
                "rating": 5,
                "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "user": 1,
            },
            {
                "game_id": 2,
                "id": 2,
                "rating": 4,
                "review_text": "Lectus vestibulum mattis ullamcorper velit sed ullamcorper.",
                "user": 1,
            },
            {
                "game_id": 3,
                "id": 3,
                "rating": 3,
                "review_text": "Vivamus at augue eget arcu. Quam pellentesque nec nam aliquam sem et tortor.",
                "user": 1,
            },
            {
                "game_id": 4,
                "id": 4,
                "rating": 4,
                "review_text": "Massa sapien faucibus et molestie ac feugiat. Risus in hendrerit gravida rutrum quisque non tellus orci ac.",
                "user": 1,
            },
        ],
        "success": True,
        "total_reviews": 7,
    }


@pytest.fixture()
def all_reviews_page_two():
    return {
        "reviews": [
            {
                "game_id": 1,
                "id": 5,
                "rating": 5,
                "review_text": "Id interdum velit laoreet id donec ultrices. Venenatis a condimentum vitae sapien pellentesque.",
                "user": 2,
            },
            {
                "game_id": 2,
                "id": 6,
                "rating": 2,
                "review_text": "Diam volutpat commodo sed egestas egestas fringilla phasellus faucibus. Scelerisque fermentum dui faucibus in. In ornare quam viverra orci.",
                "user": 2,
            },
            {
                "game_id": 3,
                "id": 7,
                "rating": 5,
                "review_text": "Quis viverra nibh cras pulvinar mattis nunc sed blandit libero. Sit amet commodo nulla facilisi.",
                "user": 2,
            },
        ],
        "success": True,
        "total_reviews": 7,
    }


@pytest.fixture()
def review_1():
    return {
        "review": {
            "game_id": 1,
            "id": 1,
            "rating": 5,
            "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "user": 1,
        },
        "success": True,
    }


@pytest.fixture()
def all_games_page_one():
    return {
        "success": True,
        "games": [
            {
                "id": 1,
                "title": "Wingspan",
                "description": "Attract a beautiful and diverse collection of birds to your aviary.",
                "min_player_count": 1,
                "max_player_count": 5,
                "play_time_minutes": 50,
                "release_date": "2019-09-01",
                "age": 10,
                "weight": 2.55,
                "genre": 1,
                "designer": 6,
                "publisher": 6,
                "image_link": "https://boardgamegeek.com/image/4458123/wingspan",
                "avg_rating": 5.0,
            },
            {
                "id": 2,
                "title": "7 Wonders Duel",
                "description": "Science? Military? What will you draft to win this head-to-head version of 7 Wonders?",
                "min_player_count": 2,
                "max_player_count": 2,
                "play_time_minutes": 30,
                "release_date": "2018-01-01",
                "age": 10,
                "weight": 2.22,
                "genre": 1,
                "designer": 5,
                "publisher": 5,
                "image_link": "https://cf.geekdo-images.com/zdagMskTF7wJBPjX74XsRw__itemrep/img/x5L93n_pSsxfFZ0Ir-JqtjLf-Jw=/fit-in/246x300/filters:strip_icc()/pic2576399.jpg",
                "avg_rating": 3.0,
            },
            {
                "id": 3,
                "title": "Parks",
                "description": "Hike through National Parks tiles, collecting memories and admiring gorgeous scenery.",
                "min_player_count": 1,
                "max_player_count": 5,
                "play_time_minutes": 40,
                "release_date": "2019-01-01",
                "age": 10,
                "weight": 2.16,
                "genre": 3,
                "designer": 4,
                "publisher": 4,
                "image_link": "https://cf.geekdo-images.com/mF2cSNRk2O6HtE45Sl9TcA__opengraph/img/uoYOX2JqGtmeJ6o5wMmfypahWEs=/fit-in/1200x630/filters:strip_icc()/pic4852372.jpg",
                "avg_rating": 4.0,
            },
            {
                "id": 4,
                "title": "Pandemic",
                "description": "Your team of experts must prevent the world from succumbing to a viral pandemic.",
                "min_player_count": 1,
                "max_player_count": 4,
                "play_time_minutes": 45,
                "release_date": "2008-06-01",
                "age": 8,
                "weight": 2.41,
                "genre": 2,
                "designer": 3,
                "publisher": 3,
                "image_link": "https://cdn.waterstones.com/override/v5/large/0681/7067/0681706711003.jpg",
                "avg_rating": 4.0,
            },
            {
                "id": 5,
                "title": "Terraforming Mars",
                "description": "Compete with rival CEOs to make Mars habitable and build your corporate empire.",
                "min_player_count": 1,
                "max_player_count": 5,
                "play_time_minutes": 120,
                "release_date": "2016-01-01",
                "age": 12,
                "weight": 3.25,
                "genre": 1,
                "designer": 2,
                "publisher": 2,
                "image_link": "https://www.boardgamequest.com/wp-content/uploads/2016/11/Terraforming-Mars-300x300.jpg",
                "avg_rating": None,
            },
        ],
        "total_games": 6,
    }


@pytest.fixture()
def all_games_page_two():
    return {
        "games": [
            {
                "age": 10,
                "avg_rating": None,
                "description": "Bluff (and call bluffs!) to victory in this card game with no third chances.",
                "designer": 1,
                "genre": 3,
                "id": 6,
                "image_link": "https://m.media-amazon.com/images/I/61JeFo5pWVL._AC_SY879_.jpg",
                "max_player_count": 6,
                "min_player_count": 2,
                "play_time_minutes": 15,
                "publisher": 1,
                "release_date": "2013-11-01",
                "title": "Coup",
                "weight": 2.1,
            }
        ],
        "success": True,
        "total_games": 6,
    }


@pytest.fixture()
def game_1():
    return {
        "average_rating": 5.0,
        "game": {
            "age": 10,
            "description": "Attract a beautiful and diverse collection of birds to your aviary.",
            "designer": 6,
            "genre": 1,
            "id": 1,
            "image_link": "https://boardgamegeek.com/image/4458123/wingspan",
            "max_player_count": 5,
            "min_player_count": 1,
            "play_time_minutes": 50,
            "publisher": 6,
            "release_date": "2019-09-01",
            "title": "Wingspan",
            "weight": 2.55,
        },
        "success": True,
    }


@pytest.fixture()
def reviews_for_game_1():
    return {
        "average_rating": 5.0,
        "game_id": 1,
        "reviews": [
            {
                "game_id": 1,
                "id": 1,
                "rating": 5,
                "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "user": 1,
            },
            {
                "game_id": 1,
                "id": 5,
                "rating": 5,
                "review_text": "Id interdum velit laoreet id donec ultrices. Venenatis a condimentum vitae sapien pellentesque.",
                "user": 2,
            },
        ],
        "success": True,
        "total_review": 2,
    }


@pytest.fixture()
def new_game_response():
    return {
        "created": 7,
        "games": [
            {
                "age": 10,
                "description": "Bluff (and call bluffs!) to victory in this card game with no third chances.",
                "designer": 1,
                "genre": 3,
                "id": 6,
                "image_link": "https://m.media-amazon.com/images/I/61JeFo5pWVL._AC_SY879_.jpg",
                "max_player_count": 6,
                "min_player_count": 2,
                "play_time_minutes": 15,
                "publisher": 1,
                "release_date": "2013-11-01",
                "title": "Coup",
                "weight": 2.1,
            },
            {
                "age": 14,
                "description": "Vanquish monsters with strategic cardplay in a 25-scenario Gloomhaven campaign.",
                "designer": 1,
                "genre": 3,
                "id": 7,
                "image_link": "https://cf.geekdo-images.com/_HhIdavYW-hid20Iq3hhmg__itemrep/img/a4ec0KY1ksmrKP_2lom7qzCQw_U=/fit-in/246x300/filters:strip_icc()/pic5055631.jpg",
                "max_player_count": 4,
                "min_player_count": 1,
                "play_time_minutes": 120,
                "publisher": 1,
                "release_date": "2020-01-01",
                "title": "Gloomhaven: Jaws of the Lion",
                "weight": 3.61,
            },
        ],
        "success": True,
        "total_games": 7,
    }


@pytest.fixture()
def update_game_response():
    return {
        "games": [
            {
                "age": 10,
                "description": "Bluff (and call bluffs!) to victory in this card game with no third chances.",
                "designer": 1,
                "genre": 3,
                "id": 6,
                "image_link": "https://m.media-amazon.com/images/I/61JeFo5pWVL._AC_SY879_.jpg",
                "max_player_count": 3,
                "min_player_count": 2,
                "play_time_minutes": 15,
                "publisher": 1,
                "release_date": "2013-11-01",
                "title": "Coup",
                "weight": 2.1,
            }
        ],
        "success": True,
        "total_games": 6,
        "updated": 6,
    }


@pytest.fixture()
def delete_game_response():
    return {
        "deleted": 1,
        "games": [
            {
                "age": 10,
                "description": "Science? Military? What will you draft to win this head-to-head version of 7 Wonders?",
                "designer": 5,
                "genre": 1,
                "id": 2,
                "image_link": "https://cf.geekdo-images.com/zdagMskTF7wJBPjX74XsRw__itemrep/img/x5L93n_pSsxfFZ0Ir-JqtjLf-Jw=/fit-in/246x300/filters:strip_icc()/pic2576399.jpg",
                "max_player_count": 2,
                "min_player_count": 2,
                "play_time_minutes": 30,
                "publisher": 5,
                "release_date": "2018-01-01",
                "title": "7 Wonders Duel",
                "weight": 2.22,
            },
            {
                "age": 10,
                "description": "Hike through National Parks tiles, collecting memories and admiring gorgeous scenery.",
                "designer": 4,
                "genre": 3,
                "id": 3,
                "image_link": "https://cf.geekdo-images.com/mF2cSNRk2O6HtE45Sl9TcA__opengraph/img/uoYOX2JqGtmeJ6o5wMmfypahWEs=/fit-in/1200x630/filters:strip_icc()/pic4852372.jpg",
                "max_player_count": 5,
                "min_player_count": 1,
                "play_time_minutes": 40,
                "publisher": 4,
                "release_date": "2019-01-01",
                "title": "Parks",
                "weight": 2.16,
            },
            {
                "age": 8,
                "description": "Your team of experts must prevent the world from succumbing to a viral pandemic.",
                "designer": 3,
                "genre": 2,
                "id": 4,
                "image_link": "https://cdn.waterstones.com/override/v5/large/0681/7067/0681706711003.jpg",
                "max_player_count": 4,
                "min_player_count": 1,
                "play_time_minutes": 45,
                "publisher": 3,
                "release_date": "2008-06-01",
                "title": "Pandemic",
                "weight": 2.41,
            },
            {
                "age": 12,
                "description": "Compete with rival CEOs to make Mars habitable and build your corporate empire.",
                "designer": 2,
                "genre": 1,
                "id": 5,
                "image_link": "https://www.boardgamequest.com/wp-content/uploads/2016/11/Terraforming-Mars-300x300.jpg",
                "max_player_count": 5,
                "min_player_count": 1,
                "play_time_minutes": 120,
                "publisher": 2,
                "release_date": "2016-01-01",
                "title": "Terraforming Mars",
                "weight": 3.25,
            },
            {
                "age": 10,
                "description": "Bluff (and call bluffs!) to victory in this card game with no third chances.",
                "designer": 1,
                "genre": 3,
                "id": 6,
                "image_link": "https://m.media-amazon.com/images/I/61JeFo5pWVL._AC_SY879_.jpg",
                "max_player_count": 6,
                "min_player_count": 2,
                "play_time_minutes": 15,
                "publisher": 1,
                "release_date": "2013-11-01",
                "title": "Coup",
                "weight": 2.1,
            },
        ],
        "success": True,
        "total_games": 5,
    }


# =====================
#  Error responses
# =====================


@pytest.fixture()
def not_found_error():
    return {"success": False, "error": 404, "message": "Not found"}
