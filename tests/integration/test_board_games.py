def test_get_all_games(client, all_games_page_one):
    response = client.get("/api/games")
    assert response.status_code == 200
    assert response.get_json() == all_games_page_one


def test_get_all_games_pagination(client, all_games_page_two):
    response = client.get("/api/games", query_string={"page": 2})
    assert response.status_code == 200
    assert response.get_json() == all_games_page_two


def test_get_all_games_raises_not_found_error(client, not_found_error):
    response = client.get("/api/games", query_string={"page": 666})
    assert response.status_code == 404
    assert response.get_json() == not_found_error


def test_get_game_by_id(client, game_1):
    response = client.get("/api/games/1")
    assert response.status_code == 200
    assert response.get_json() == game_1


def test_get_reviews_for_game(client, reviews_for_game_1):
    response = client.get("/api/games/1/reviews")
    assert response.status_code == 200
    assert response.get_json() == reviews_for_game_1


def test_create_new_game(client, new_game_response, mocker):
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["post:games"]},
    )
    response = client.post(
        "/api/games",
        json={
            "title": "Gloomhaven: Jaws of the Lion",
            "description": "Vanquish monsters with strategic cardplay in a 25-scenario Gloomhaven campaign.",
            "min_player_count": 1,
            "max_player_count": 4,
            "play_time_minutes": 120,
            "release_date": "2020-01-01",
            "age": 14,
            "weight": 3.61,
            "genre_id": 3,
            "designer_id": 1,
            "publisher_id": 1,
            "image_link": "https://cf.geekdo-images.com/_HhIdavYW-hid20Iq3hhmg__itemrep/img/a4ec0KY1ksmrKP_2lom7qzCQw_U=/fit-in/246x300/filters:strip_icc()/pic5055631.jpg",
        },
        query_string={"page": 2},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 201
    assert response.get_json() == new_game_response


def test_update_game(client, update_game_response, mocker):
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:games"]},
    )
    response = client.patch(
        "/api/games/6",
        json={"max_player_count": 3},
        query_string={"page": 2},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == update_game_response


def test_delete_game(client, delete_game_response, mocker):
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["delete:games"]},
    )
    response = client.delete(
        "/api/games/1",
        query_string={"page": 1},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == delete_game_response
