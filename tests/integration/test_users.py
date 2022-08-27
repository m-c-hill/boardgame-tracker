def test_get_reviews_by_user(client):
    client.get("/api/users/1/reviews")


def test_get_reviews_by_user_raises_exception(client):
    client.get("/api/users/666/reviews")
