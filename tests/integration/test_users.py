def test_get_reviews_by_user(client, reviews_for_user_1):
    response = client.get("/api/users/1/reviews")
    assert response.status_code == 200
    assert response.get_json() == reviews_for_user_1


def test_get_reviews_by_user_raises_exception(client, not_found_error):
    response = client.get("/api/users/666/reviews")
    assert response.status_code == 404
    assert response.get_json() == not_found_error
