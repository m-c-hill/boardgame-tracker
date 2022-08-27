import pytest

from app.models.collection import Collection


def test_create_collection():
    collection = Collection(user_id=1)

    assert collection.user_id == 1


def test_add_new_game_to_collection(collection, game_id):
    assert len(collection.games) == 0

    collection.add(game_id)
    assert collection.includes_game(game_id)
    assert len(collection.games) == 1


def test_add_existing_game_to_collection(collection, game_id):
    assert len(collection.games) == 0

    collection.add(game_id)
    assert collection.includes_game(game_id)
    assert len(collection.games) == 1

    collection.add(game_id)
    assert len(collection.games) == 1


def test_remove_game_from_collection(collection, game_id):
    assert len(collection.games) == 0

    collection.add(game_id)
    assert collection.includes_game(game_id)
    assert len(collection.games) == 1

    collection.remove(game_id)
    assert len(collection.games) == 0


def test_remove_game_from_collection_invalid(collection, game_id):
    assert len(collection.games) == 0

    collection.add(game_id)
    assert collection.includes_game(game_id)
    assert len(collection.games) == 1

    invalid_game_id = 2
    collection.remove(invalid_game_id)
    assert len(collection.games) == 1
