def test_get_all_games_in_collection(client, collection_1_games, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    response = client.get("/api/collections/1/games")
    assert response.status_code == 200
    assert response.get_json() == collection_1_games


def test_get_all_games_raises_exception_no_collection(client, not_found_error):
    response = client.get("/api/collections/666/games")
    assert response.status_code == 404
    assert response.get_json() == not_found_error


# TODO: similar issue with list
def test_add_game_to_collection(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:collection"]},
    )
    response = client.patch(
        "/api/collections/1/games",
        json={"game_id": 4, "action": "add"},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "action": "add",
        "collection_id": 1,
        "games_in_collection": [1, 2, 3, 4],
        "game_id": 4,
        "success": True,
    }


def test_remove_game_from_collection(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:collection"]},
    )
    response = client.patch(
        "/api/collections/1/games",
        json={"game_id": 1, "action": "remove"},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "action": "remove",
        "collection_id": 1,
        "games_in_collection": [2, 3],
        "game_id": 1,
        "success": True,
    }


def test_toggle_collection_privacy(client, mocker):
    mocker.patch("app.main.routes.collections.check_user_id", return_value=True)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:collection"]},
    )
    response = client.patch(
        "/api/collections/1/privacy", headers={"Authorization": "Bearer x"}
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "collection_id": 1,
        "private": False,
    }
