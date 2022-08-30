def test_get_reviews_by_user(client, reviews_for_user_1):
    response = client.get("/api/users/admin/reviews")
    assert response.status_code == 200
    assert response.get_json() == reviews_for_user_1


def test_get_reviews_by_user_raises_exception(client, bad_request):
    response = client.get("/api/users/other_user/reviews")
    assert response.status_code == 400
    assert response.get_json() == bad_request
