def test_get_all_games(client, all_games_page_one):
    response = client.get("/api/games", query_string={"page": 1})
    assert response.status_code == 200
    assert response == all_games_page_one


def test_get_all_games_pagination(client, all_games_page_two):
    response = client.get("/api/games", query_string={"page": 2})
    assert response.status_code == 200
    assert response == all_games_page_two


def test_get_all_games_raises_not_found_error(client, not_found_error):
    response = client.get("/api/games", query_string={"page": 666})
    assert response.status_code == 404
    assert response == not_found_error


def test_get_game_by_id(client, game_1):
    response = client.get("/api/games/1")
    assert response.status_code == 200
    assert response == game_1


def test_get_reviews_for_game(client, reviews_for_game_1):
    response = client.get("/api/games/1/reviews")
    assert response.status_code == 200
    assert response == reviews_for_game_1


def test_create_new_game(client, new_game_response):
    response = client.post("/api/games", json={})  # TODO
    assert response.status_code == 201
    assert response.get_json() == new_game_response


def test_update_game(client, update_game_response):
    response = client.patch("/api/games/1", json={})
    assert response.status_code == 200
    assert response.get_json == update_game_response


def test_delete_game(client, delete_game_response):
    response = client.delete("/api/games/1")
    assert response.status_code == 200
    assert response.get_json() == delete_game_response
