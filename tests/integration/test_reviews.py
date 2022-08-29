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


def test_create_review(client, mocker):
    mocker.patch("app.main.routes.reviews.get_current_user_id", return_value=1)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["post:reviews"]},
    )
    response = client.post(
        "/api/reviews",
        json={"game_id": 5, "review_text": "Really great", "rating": 4},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 201
    assert response.get_json() == {
        "success": True,
        "created": 8,
        "reviews": [
            {
                "id": 8,
                "user": 1,
                "game_id": 5,
                "rating": 4,
                "review_text": "Really great",
            }
        ],
        "total_reviews_for_game": 1,
    }


def test_update_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:reviews"]},
    )
    response = client.patch(
        "/api/reviews/1", json={"rating": 1}, headers={"Authorization": "Bearer x"}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "reviews": [
            {
                "game_id": 1,
                "id": 1,
                "rating": 1,
                "review_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                "user": 1,
            },
            {
                "game_id": 1,
                "id": 5,
                "rating": 5,
                "review_text": "Id interdum velit laoreet id donec ultrices. Venenatis a condimentum vitae sapien pellentesque.",
                "user": 2,
            },
        ],
        "success": True,
        "total_reviews_for_game": 2,
        "updated": 1,
    }


def test_delete_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["delete:reviews"]},
    )
    response = client.delete("/api/reviews/3", headers={"Authorization": "Bearer x"})
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


def test_like_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    mocker.patch("app.main.routes.reviews.get_current_user_id", return_value=1)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:reactions"]},
    )
    response = client.patch(
        "/api/reviews/2/reactions",
        json={"like": True},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "review_id": 2,
        "likes": 1,
        "dislikes": 0,
    }


def test_dislike_review(client, mocker):
    mocker.patch("app.main.routes.reviews.check_user_id", return_value=True)
    mocker.patch("app.main.routes.reviews.get_current_user_id", return_value=1)
    mocker.patch(
        "app.utils.auth0.verify_decode_jwt",
        return_value={"permissions": ["patch:reactions"]},
    )
    response = client.patch(
        "/api/reviews/2/reactions",
        json={"dislike": True},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "success": True,
        "review_id": 2,
        "likes": 0,
        "dislikes": 1,
    }
