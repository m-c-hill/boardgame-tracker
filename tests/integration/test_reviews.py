def test_get_all_reviews(client):
    response = client.get("/api/reviews")

def test_get_review_by_id(client):
    response = client.get("/api/reviews/1")

def test_create_review(client):
    response = client.post("/api/reviews", json={})

def test_update_review(client):
    response = client.patch("/api/reviews/1", json={})

def test_update_review_raises_auth_error(client):
    response = client.patch("/api/reviews/1", json={})

def test_delete_review(client):
    response = client.delete("/api/reviews/1", json={})

def test_delete_review_raises_auth_error(client):
    response = client.delete("/api/reviews/1", json={})

def test_get_reactions_for_review(client):
    response = client.get("/api/reviews/1/reactions")

def test_like_review(client):
    response = client.patch("/api/reviews/1/reactions", json={"like": True})

def test_like_review(client):
    response = client.patch("/api/reviews/1/reactions", json={"dislike": True})
