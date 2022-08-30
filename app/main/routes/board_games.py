from flask import abort, jsonify, request
from numpy import mean

from ...domain.board_game import BoardGame
from ...domain.review import Review
from ...utils.auth0 import requires_auth
from ...utils.requests import paginate_items
from .. import main
from . import GAMES_PER_PAGE, REVIEWS_PER_PAGE


@main.route("/")
def home():
    return "Board Game Tracker"


@main.route("/games")
def get_all_games():
    games = BoardGame.query.order_by(BoardGame.id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    if not current_games:
        abort(404)

    games_with_avg_rating = []
    for game in current_games:
        reviews = Review.query.filter_by(board_game=game["id"]).all()
        game["avg_rating"] = (
            mean([r.rating for r in reviews]) if len(reviews) > 0 else None
        )
        games_with_avg_rating.append(game)

    return jsonify(
        {"success": True, "games": games_with_avg_rating, "total_games": len(games)}
    )


@main.route("/games/<int:game_id>")
def get_game_by_id(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)

    reviews_for_game = Review.query.filter_by(board_game=game_id).all()
    average_rating = (
        mean([r.rating for r in reviews_for_game]) if reviews_for_game else None
    )

    return jsonify(
        {"success": True, "game": game.format(), "average_rating": average_rating}
    )


@main.route("/games/<int:game_id>/reviews")
def get_reviews_for_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()
    if game is None:
        abort(404)

    reviews_for_game = Review.query.filter_by(board_game=game_id).all()

    if reviews_for_game:
        average_rating = mean([r.rating for r in reviews_for_game])
    else:
        average_rating = None

    reviews = paginate_items(request, reviews_for_game, REVIEWS_PER_PAGE)

    return jsonify(
        {
            "success": True,
            "game_id": game_id,
            "reviews": reviews,
            "average_rating": average_rating,
            "total_review": len(reviews_for_game),
        }
    )


@main.route("/games", methods=["POST"])
@requires_auth("post:games")
def create_game():
    body = request.get_json()
    try:
        game = BoardGame(
            title=body.get("title"),
            description=body.get("description"),
            min_player_count=body.get("min_player_count"),
            max_player_count=body.get("max_player_count"),
            play_time_minutes=body.get("play_time_minutes"),
            release_date=body.get("release_date"),
            age=body.get("age"),
            weight=body.get("weight"),
            genre_id=body.get("genre_id"),
            designer_id=body.get("designer_id"),
            publisher_id=body.get("publisher_id"),
            image_link=body.get("image_link"),
        )
        game.insert()

        games = BoardGame.query.order_by(BoardGame.id).all()
        formatted_games = paginate_items(request, games, GAMES_PER_PAGE)

        return (
            jsonify(
                {
                    "success": True,
                    "created": game.id,
                    "games": formatted_games,
                    "total_games": len(games),
                }
            ),
            201,
        )

    except:
        abort(422)


@main.route("/games/<int:game_id>", methods=["PATCH"])
@requires_auth("patch:games")
def update_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)

    updates = request.get_json()

    try:
        game.title = updates.get("title", game.title)
        game.description = updates.get("description", game.description)
        game.min_player_count = updates.get("min_player_count", game.min_player_count)
        game.max_player_count = updates.get("max_player_count", game.max_player_count)
        game.play_time_minutes = updates.get(
            "play_time_minutes", game.play_time_minutes
        )
        game.release_date = updates.get("release_date", game.release_date)
        game.age = updates.get("age", game.age)
        game.weight = updates.get("weight", game.weight)
        game.genre = updates.get("genre", game.genre)
        game.designer = updates.get("designer", game.designer)
        game.publisher = updates.get("publisher", game.publisher)
        game.image_link = updates.get("image_link", game.image_link)
        game.update()

        games = BoardGame.query.order_by(BoardGame.id).all()
        formatted_games = paginate_items(request, games, GAMES_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "updated": game.id,
                "games": formatted_games,
                "total_games": len(games),
            }
        )
    except:
        abort(422)


@main.route("/games/<int:game_id>", methods=["DELETE"])
@requires_auth("delete:games")
def delete_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)

    reviews = Review.query.filter_by(board_game=game_id).all()

    try:
        for review in reviews:
            review.delete()
        game.delete()

        games = BoardGame.query.order_by(BoardGame.id).all()
        formatted_games = paginate_items(request, games, GAMES_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "deleted": game.id,
                "games": formatted_games,
                "total_games": len(games),
            }
        )
    except:
        abort(422)
