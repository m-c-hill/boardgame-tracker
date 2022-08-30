from flask import abort, jsonify, request

from ...domain.review import Review
from ...domain.user import User
from ...utils.requests import paginate_items
from .. import main
from . import REVIEWS_PER_PAGE


@main.route("users/<string:username>/reviews")
def get_reviews_by_user(username):
    user = User.query.filter_by(username=username).one_or_none()

    if user is None:
        abort(400)

    reviews = Review.query.filter_by(user=user.id).all()

    if reviews is None:
        abort(404)

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
