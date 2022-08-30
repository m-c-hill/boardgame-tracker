from app.domain.review import Review


def test_create_review():
    review = Review(
        game_id=1,
        review_text="Wingspan isn't as heavy as I expected but this is not a bad thing. Its ease and speed of play mean that the game is welcoming, without leaving experienced players bored or feeling like they must hold back.",
        rating=5,
        user_id=1,
    )

    assert review.board_game == 1
    assert (
        review.review_text
        == "Wingspan isn't as heavy as I expected but this is not a bad thing. Its ease and speed of play mean that the game is welcoming, without leaving experienced players bored or feeling like they must hold back."
    )
    assert review.rating == 5
    assert review.user == 1


def test_review_rating_exceeds_max_rating():
    pass


def test_review_rating_below_min_rating():
    pass


def test_like_review(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.like_review(user_id)
    assert review.likes == 1
    assert review.dislikes == 0


def test_dislike_review(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.dislike_review(user_id)
    assert review.likes == 0
    assert review.dislikes == 1


def test_liking_review_removes_dislike(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.dislike_review(user_id)
    assert review.likes == 0
    assert review.dislikes == 1
    review.like_review(user_id)
    assert review.likes == 1
    assert review.dislikes == 0


def test_disliking_review_removes_like(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.like_review(user_id)
    assert review.likes == 1
    assert review.dislikes == 0
    review.dislike_review(user_id)
    assert review.likes == 0
    assert review.dislikes == 1


def test_can_only_like_review_once(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.like_review(user_id)
    assert review.likes == 1
    assert review.dislikes == 0
    review.like_review(user_id)
    assert review.likes == 1
    assert review.dislikes == 0


def test_can_only_dislike_review_once(review, user_id):
    assert review.likes == 0
    assert review.dislikes == 0
    review.dislike_review(user_id)
    assert review.likes == 0
    assert review.dislikes == 1
    review.dislike_review(user_id)
    assert review.likes == 0
    assert review.dislikes == 1
