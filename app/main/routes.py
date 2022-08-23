from multiprocessing import current_process
from . import main

from flask import abort, jsonify, request

from numpy import mean

from app.models.models import BoardGame, Review, User, Publisher, Genre, Designer
from ..utils import paginate_items

GAMES_PER_PAGE = 10
REVIEWS_PER_PAGE = 5

# ========================
#  Board Game Enpoints
# ========================

# TODO: sort_by/order_by request params: https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/
@main.route("/games")
def get_all_games():
    games = BoardGame.query.all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)
    # TODO: add average rating for each game

    if not current_games:
        abort(404)

    return jsonify({"success": True, "games": current_games, "total_games": len(games)})


@main.route("/games/<int:game_id>")
def get_game_by_id(game_id):
    game = BoardGame.query.filter_by(id=game_id)

    reviews_for_game = Review.query.filter_by(board_game=game_id).all()
    average_rating = mean([r.rating for r in reviews_for_game]) if reviews_for_game else None

    if game is None:
        abort(404)

    return jsonify({"success": True, "game": game.format(), "average_rating": average_rating})


@main.route("/games/<int:game_id>/reviews")
def get_reviews_for_game(game_id):
    reviews_for_game = Review.query.filter_by(board_game=game_id).all()

    if not reviews_for_game:
        abort(404)

    average_rating = mean([r.rating for r in reviews_for_game])
    reviews = paginate_items(request, reviews_for_game, REVIEWS_PER_PAGE)

    return jsonify({"success": True, "game_id": game_id, "reviews": reviews, "average_rating": average_rating, "total_review": len(reviews_for_game)})


# TODO
@main.route("/games", methods=["POST"])
def create_game():
    return


# TODO
@main.route("/games/<int:game_id>", methods=["PATCH"])
def update_game(game_id):
    return


@main.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)
    
    reviews = Review.query.filter_by(board_game=game_id).all()

    try:
        for review in reviews:
            review.delete()
        game.delete()

        return jsonify({"success": True, "deleted": game.id})
    except:
        abort(422)


# ========================
#  Review Endpoints
# ========================


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
def create_review():
    body = request.get_json()

    try:
        review = Review(game_id=body.get("game_id"), review_text=body.get("review_text"), rating=body.get("rating"), user_id=body.get("user_id"))
        review.insert()

        reviews = Review.query.filter_by(board_game=body.get("game_id")).order_by(Review.id).all()
        formatted_reviews = paginate_items()

        return jsonify(
            {"success": True, "created": review.id, "reviews": formatted_reviews}
        )

    except:  # TODO: specific exception
        abort(422)


#TODO
@main.route("/reviews/<int:review_id>", methods=["PATCH"])
def update_review(review_id):
    return


@main.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)
    
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
def react_to_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    body = request.get_json()
    try:
        if body.get("like"):
            review.likes += 1
        elif body.get("dislikes"):
            review.dislikes += 1
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


# ========================
#  Genre Endpoints
# ========================


@main.route("/genres", methods=["GET"])
def get_genres():
    genres = Genre.query.order_by(Genre.id).all()
    formatted_genres = {genre.id: genre.name for genre in genres}

    if len(formatted_genres) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "genres": formatted_genres,
            "total_genres": len(formatted_genres),
        }
    )


@main.route("/genres/<int:genre_id>")
def get_genre_by_id(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    games = BoardGame.query.filter_by(genre=genre_id).all()

    return jsonify(
        {"success": True, "genre": genre.format(), "total_games": len(games)}
    )


@main.route("/genres/<int:genre_id>/games")
def get_games_for_genre(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    games = BoardGame.query.filter_by(genre=genre_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "genre": genre.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/genres", methods=["POST"])
def create_genre():
    body = request.get_json()

    try:
        genre = Genre(name=body.get("name"), description=body.get("description"))
        genre.insert()

        genres = Genre.query.order_by(Genre.id).all()
        formatted_genres = {genre.id: genre.name for genre in genres}

        return jsonify(
            {"success": True, "created": genre.id, "genres": formatted_genres}
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/genres/<int:genre_id>", methods=["PATCH"])
def update_genre(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    updates = request.get_json()

    try:
        genre.name = updates.get("name", genre.name)
        genre.description = updates.get("description", genre.description)
        genre.update()

        genres = Genre.query.order_by(Genre.id).all()
        formatted_genres = {genre.id: genre.name for genre in genres}

        return jsonify(
            {"success": True, "updated": genre.id, "genres": formatted_genres}
        )
    except:
        abort(422)


# ========================
#  Publisher Endpoints
# ========================


@main.route("/publishers", methods=["GET"])
def get_publishers():
    publishers = Publisher.query.order_by(Publisher.id).all()
    formatted_publishers = {publisher.id: publisher.name for publisher in publishers}

    if len(formatted_publishers) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "publishers": formatted_publishers,
            "total_publishers": len(formatted_publishers),
        }
    )


@main.route("/publishers/<int:publisher_id>")
def get_publisher_by_id(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    games = BoardGame.query.filter_by(publisher=publisher_id).all()

    return jsonify(
        {"success": True, "publisher": publisher.format(), "total_games": len(games)}
    )


@main.route("/publishers/<int:publisher_id>/games")
def get_games_for_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    games = BoardGame.query.filter_by(publisher=publisher_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "publisher": publisher.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/publishers", methods=["POST"])
def create_publisher():
    body = request.get_json()

    try:
        publisher = Publisher(name=body.get("name"))
        publisher.insert()

        publishers = Publisher.query.order_by(Publisher.id).all()
        formatted_publishers = {
            publisher.id: publisher.name for publisher in publishers
        }

        return jsonify(
            {
                "success": True,
                "created": publisher.id,
                "publishers": formatted_publishers,
            }
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/publishers/<int:publisher_id>", methods=["PATCH"])
def update_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    updates = request.get_json()

    try:
        publisher.name = updates.get("name", publisher.name)
        publisher.update()

        publishers = Publisher.query.order_by(Publisher.id).all()
        formatted_publishers = {
            publisher.id: publisher.name for publishers in publishers
        }

        return jsonify(
            {
                "success": True,
                "updated": publisher.id,
                "publishers": formatted_publishers,
            }
        )
    except:
        abort(422)


# ========================
#  Designer Endpoints
# ========================


@main.route("/designers", methods=["GET"])
def get_designers():
    designers = Designer.query.order_by(Designer.id).all()
    formatted_designers = {designer.id: designer.name for designer in designers}

    if len(formatted_designers) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "designers": formatted_designers,
            "total_designers": len(formatted_designers),
        }
    )


@main.route("/designers/<int:designer_id>")
def get_designer_by_id(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    games = BoardGame.query.filter_by(designer=designer_id).all()

    return jsonify(
        {"success": True, "designer": designer.format(), "total_games": len(games)}
    )


@main.route("/designers/<int:designer_id>/games")
def get_games_for_designer(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    games = BoardGame.query.filter_by(designer=designer_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "designer": designer.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/designers", methods=["POST"])
def create_designer():
    body = request.get_json()

    try:
        designer = Designer(
            first_name=body.get("first_name"), last_name=body.get("last_name")
        )
        designer.insert()

        designers = Designer.query.order_by(Designer.id).all()
        formatted_designers = {
            designer.id: {
                "first_name": designer.first_name,
                "last_name": designer.last_name,
            }
            for designer in designers
        }

        return jsonify(
            {"success": True, "created": designer.id, "designers": formatted_designers}
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/designers/<int:designer_id>", methods=["PATCH"])
def update_designer(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    updates = request.get_json()

    try:
        designer.first_name = updates.get("first_name", designer.first_name)
        designer.last_name = updates.get("last_name", designer.last_name)
        designer.update()

        designers = Designer.query.order_by(Designer.id).all()
        formatted_designers = {
            designer.id: {
                "first_name": designer.first_name,
                "last_name": designer.last_name,
            }
            for designer in designers
        }

        return jsonify(
            {"success": True, "updated": designer.id, "designers": formatted_designers}
        )

    except:
        abort(422)


# ===========================
#  Search Endpoints
# ===========================

# TODO: design these endpoints
# POST search for games by name

# POST advanced search for games with filters
