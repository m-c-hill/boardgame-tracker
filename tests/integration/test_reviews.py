def test_get_all_reviews(client, all_reviews_page_one):
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert response.get_json() == all_reviews_page_one


def test_get_all_reviews_pagination(client, all_reviews_page_two):
    response = client.get("/api/reviews", query_string={"page": 2})
    assert response.status_code == 200
    assert response.get_json() == all_reviews_page_two


def test_get_all_reviews_pagination_raises_not_found_error(client, not_found_error):
    response = client.get("/api/reviews", query_string={"page": 666})
    assert response.status_code == 404
    assert response.get_json() == not_found_error


def test_get_review_by_id(client, review_1):
    response = client.get("/api/reviews/1")
    assert response.status_code == 200
    assert response.get_json() == review_1


# TODO
def test_create_review(client, mocker):
    mocker.patch("app.main.routes.reviews.get_current_user_id", return_value=1)
    response = client.post("/api/reviews", json={})  # TODO
    assert response.status_code == 201
    assert response.get_json() == ""  # TODO


# TODO
def test_update_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    response = client.patch("/api/reviews/1", json={})  # TODO
    assert response.status_code == 200
    assert response.get_json() == ""  # TODO


# TODO
def test_delete_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    response = client.delete("/api/reviews/3")
    assert response.status_code == 200
    assert response.get_json() == {"success": True, "deleted": 3}


def test_get_reactions_for_review(client):
    response = client.get("/api/reviews/1/reactions")
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "review_id": 1,
        "likes": 9,
        "dislikes": 3,
    }


# TODO (auth)
def test_like_review(client):
    response = client.patch("/api/reviews/2/reactions", json={"like": True})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "review_id": 2,
        "likes": 1,
        "dislikes": 0,
    }


# TODO (auth)
def test_dislike_review(client):
    response = client.patch("/api/reviews/2/reactions", json={"dislike": True})
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "review_id": 2,
        "likes": 0,
        "dislikes": 1,
    }
