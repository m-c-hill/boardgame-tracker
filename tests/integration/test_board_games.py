from app.models.board_game import BoardGame


def test_get_all_games(client):
    response = client.get("/api/games")

def test_get_game_by_id(client):
    response = client.get("/api/games/1")

def test_get_reviews_for_game(client):
    response = client.get("/api/games/1/reviews")

def test_create_new_game(client):
    response = client.post("/api/games", json={})

def test_update_game(client):
    response = client.patch("/api/games/1", json={})

def test_delete_game(client):
    response = client.delete("/api/games/1", json={})

def test_delete_invalid_game_raises_error(client):
    response = client.delete("/api/games/666", json={})