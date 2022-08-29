from flask import abort, jsonify, request

from ...models.board_game import BoardGame, Genre
from ...utils.auth0 import requires_auth
from ...utils.requests import paginate_items
from .. import main
from . import GAMES_PER_PAGE


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
@requires_auth("post:genres")
def create_genre():
    body = request.get_json()

    try:
        genre = Genre(name=body.get("name"), description=body.get("description"))
        genre.insert()

        genres = Genre.query.order_by(Genre.id).all()
        formatted_genres = {genre.id: genre.name for genre in genres}

        return (
            jsonify({"success": True, "created": genre.id, "genres": formatted_genres}),
            201,
        )

    except:
        abort(422)


@main.route("/genres/<int:genre_id>", methods=["PATCH"])
@requires_auth("patch:genres")
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
