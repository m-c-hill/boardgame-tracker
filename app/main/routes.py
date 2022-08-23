from . import main

from ..utils import paginate_questions

# ========================
#  Board Game Enpoints
# ========================

# TODO: sort_by/order_by request params: https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/
@main.route("/games")
def get_all_games():
    return


@main.route("/games/<int:game_id>")
def get_game_by_id(game_id):
    return


@main.route("/games/<id:game_id>/reviews")
def get_reviews_for_game(game_id):
    return


@main.route("/games", methods=["POST"])
def create_game():
    return


@main.route("/games/<id:game_id>", methods=["PATCH"])
def update_game(game_id):
    return


@main.route("/games/<id:game_id>", methods=["DELETE"])
def delete_game(game_id):
    return


# ========================
#  Review Endpoints
# ========================

@main.route("/reviews")
def get_all_reviews():
    return


@main.route("/reviews/<int:review_id>")
def get_review_by_id(review_id):
    # Add average score
    return


@main.route("/reviews", methods=["POST"])
def create_review():
    return


@main.route("/reviews/<int:review_id>", methods=["PATCH"])
def update_review(review_id):
    return


@main.route("/reviews/<int:review_id>/likes", methods=["POST"])
def like_review(review_id):
    return


@main.route("/reviews/<int:review_id>/likes")
def like_review(review_id):
    return


# ========================
#  Genre Endpoints
# ========================


@main.route("/genres", methods=["GET"])
def get_genres():
    return


@main.route("/genres/<int:genre_id>")
def get_genre_by_id(genre_id):
    return


@main.route("/genres/<int:genre_id>/games")
def get_games_for_genre(genre_id):
    return


@main.route("/genres", method=["POST"])
def create_genre():
    pass


@main.route("/genres/<int:genre_id>", method=["PATCH"])
def update_genre(genre_id):
    pass


# ========================
#  Publisher Endpoints
# ========================


@main.route("/publishers", methods=["GET"])
def get_publishers():
    return


@main.route("/publishers/<int:publisher_id>")
def get_publisher_by_id(publisher_id):
    return


@main.route("/publishers/<int:publisher_id>/games")
def get_publisher_for_genre(publisher_id):
    return


@main.route("/publishers", method=["POST"])
def create_publisher():
    pass


@main.route("/publishers/<int:publisher_id>", method=["PATCH"])
def update_publisher(publisher_id):
    pass


# ========================
#  Designer Endpoints
# ========================


@main.route("/designers", methods=["GET"])
def get_designers():
    return


@main.route("/designers/<int:designer_id>")
def get_designer_by_id(designer_id):
    return


@main.route("/designers/<int:designer_id>/games")
def get_designer_for_genre(designer_id):
    return


@main.route("/designers", method=["POST"])
def create_designer():
    pass


@main.route("/designers/<int:designer_id>", method=["PATCH"])
def update_designer(designer_id):
    pass


# ===========================
#  Search Endpoints
# ===========================

# TODO: design these endpoints
# POST search for games by name

# POST advanced search for games with filters

