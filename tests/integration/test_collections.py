def test_get_all_games_in_collection(client):
    response = client.get("/api/collections/1")

def test_get_all_games_raises_exception_no_collection(client):
    response = client.get("/api/collections/666")

def test_add_game_to_collection(client):
    response = client.post("/api/collections/1", json={})

def test_add_game_to_collection_user_unauthorized(client):
    response = client.post("/api/collections/1", json={})

def test_remove_game_from_collection(client):
    response = client.delete("/api/collections/1", json={})

def test_toggle_collection_privacy(client):
    response = client.patch("/api/collections/1/privacy", json={})
