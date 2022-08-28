from flask import abort, jsonify, request

from ...models.review import Review
from ...models.user import User
from ...utils.requests import paginate_items
from .. import main
from . import REVIEWS_PER_PAGE


@main.route("users/<string:username>/reviews")
def get_reviews_by_user(username):
    user = User.query.filter_by(username=username).one_or_none()

    if user is None:
        abort(404)

    reviews = Review.query.filter_by(user=user.id).all()
    current_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

    return jsonify(
        {
            "success": True,
            "username": user.username,
            "user_id": user.auth0_id,
            "reviews": current_reviews,
            "total_reviews_by_user": len(reviews),
        }
    )
