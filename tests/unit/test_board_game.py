from datetime import date

from app.domain.board_game import BoardGame, Designer, Genre, Publisher


def test_create_board_game():
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

    assert game.title == "Wingspan"
    assert (
        game.description
        == "A card-driven, engine-building board game in which one to five players compete to attract birds to their wildlife reserves."
    )
    assert game.min_player_count == 1
    assert game.max_player_count == 5
    assert game.play_time_minutes == 60
    assert game.release_date == date(year=2020, month=9, day=17)
    assert game.age == 12
    assert game.weight == 2.5
    assert game.genre == 1
    assert game.designer == 1
    assert game.publisher == 1
    assert (
        game.image_link
        == "https://stonemaiergames.com/wp-content/uploads/2019/02/3d-wingspan-300x294.png"
    )


def test_create_genre():
    genre = Genre(
        name="Engine-builder",
        description="Players slowly build up a system of generating resources, money, or victory points.",
    )

    assert genre.name == "Engine-builder"
    assert (
        genre.description
        == "Players slowly build up a system of generating resources, money, or victory points."
    )


def test_create_designer():
    designer = Designer(first_name="Elizabeth", last_name="Hargrave")

    assert designer.first_name == "Elizabeth"
    assert designer.last_name == "Hargrave"


def test_create_publisher():
    publisher = Publisher(name="Stonemaier Games")

    assert publisher.name == "Stonemaier Games"
