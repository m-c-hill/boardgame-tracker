def test_get_all_games_in_collection(client, collection_1_games):
    response = client.get("/api/collections/1")
    assert response.status_code == 200
    assert response.get_json() == collection_1_games


def test_get_all_games_raises_exception_no_collection(client, not_found_error):
    response = client.get("/api/collections/666")
    assert response.status_code == 404
    assert response.get_json() == not_found_error


def test_add_game_to_collection(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    response = client.patch(
        "/api/collections/1/games", json={"game_id": 1, "action": "add"}
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "action": "add",
        "collection_id": 1,
        "game_id": 1,
        "success": True,
    }


def test_remove_game_from_collection(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    response = client.patch(
        "/api/collections/1/games", json={"game_id": 1, "action": "add"}
    )
    assert response.get_json() == {
        "action": "add",
        "collection_id": 1,
        "game_id": 1,
        "success": True,
    }

    response = client.patch(
        "/api/collections/1/games", json={"game_id": 1, "action": "remove"}
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "action": "remove",
        "collection_id": 1,
        "game_id": 1,
        "success": True,
    }


def test_toggle_collection_privacy(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    response = client.patch("/api/collections/1/privacy")
    assert response == 200
    assert response.get_json() == {
        "success": True,
        "collection_id": 1,
        "private": False,
    }
