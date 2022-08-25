from flask import abort, jsonify, request, session

from ...models.review import Review
from ...utils.auth0 import requires_auth
from ...utils.authentication import check_user_id, get_current_user_id
from ...utils.requests import paginate_items
from .. import main
from . import REVIEWS_PER_PAGE


@main.route("/reviews")
def get_all_reviews():
    reviews = Review.query.all()
    current_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

    if not current_reviews:
        abort(404)

    return jsonify(
        {"success": True, "reviews": current_reviews, "total_reviews": len(reviews)}
    )


@main.route("/reviews/<int:review_id>")
def get_review_by_id(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    return jsonify({"success": True, "review": review})


@main.route("/reviews", methods=["POST"])
@requires_auth("post:reviews")
def create_review():
    body = request.get_json()

    try:
        review = Review(
            game_id=body.get("game_id"),
            review_text=body.get("review_text"),
            rating=body.get("rating"),
            user_id=get_current_user_id(session),
        )
        review.insert()

        reviews = (
            Review.query.filter_by(board_game=body.get("game_id"))
            .order_by(Review.id)
            .all()
        )
        formatted_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

        return (
            jsonify(
                {
                    "success": True,
                    "created": review.id,
                    "reviews": formatted_reviews,
                    "total_reviews_for_game": len(reviews),
                }
            ),
            201,
        )

    except:
        abort(422)


@main.route("/reviews/<int:review_id>", methods=["PATCH"])
@requires_auth("patch:reviews")
def update_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    updates = request.get_json()
    try:
        review.review_text = updates.get("review_text", review.review_text)
        review.rating = updates.get("rating", review.rating)
        review.update()

        reviews = (
            Review.query.filter_by(board_game=review.get("board_game"))
            .order_by(Review.id)
            .all()
        )
        formatted_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "updated": review.id,
                "reviews": formatted_reviews,
                "total_reviews_for_game": len(reviews),
            }
        )
    except:
        abort(422)


@main.route("/reviews/<int:review_id>", methods=["DELETE"])
@requires_auth("delete:reviews")
def delete_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    try:
        review.delete()
        return jsonify({"success": True, "deleted": review.id})
    except:
        abort(422)


@main.route("/reviews/<int:review_id>/reactions")
def get_reactions_for_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    return jsonify(
        {
            "success": True,
            "review_id": review.id,
            "likes": review.likes,
            "dislikes": review.dislikes,
        }
    )


@main.route("/reviews/<int:review_id>/reactions", methods=["PATCH"])
@requires_auth("patch:reactions")
def react_to_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()
    user_id = get_current_user_id(session)

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    body = request.get_json()
    try:
        if body.get("like"):
            review.like_post(user_id)
        elif body.get("dislikes"):
            review.dislike_post(user_id)
        review.update()
        return jsonify(
            {
                "success": True,
                "review_id": review.id,
                "likes": review.likes,
                "dislikes": review.dislikes,
            }
        )
    except:
        abort(422)
