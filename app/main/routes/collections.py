from flask import abort, jsonify, request
from numpy import mean

from ...models.board_game import BoardGame
from ...models.collection import Collection
from ...utils.auth0 import requires_auth
from ...utils.authentication import check_user_id
from .. import main


@main.route("/collections/<int:collection_id>/games")
def get_games_in_collection(collection_id):
    collection = Collection.query.filter_by(id=collection_id).one_or_none()

    if collection is None:
        abort(404)

    if collection.private and not check_user_id(collection.user_id):
        abort(401)

    formatted_collection = collection.format()
    formatted_games = [
        BoardGame.query.filter_by(id=game_id).one().format()
        for game_id in formatted_collection["games"]
    ]
    formatted_collection["games"] = formatted_games

    return {
        "success": True,
        "collection": formatted_collection,
        "total_games": len(formatted_games),
    }


@main.route("/collections/<int:collection_id>/games", methods=["PATCH"])
@requires_auth("patch:collection")
def update_collection(collection_id):
    collection = Collection.query.filter_by(id=collection_id).one_or_none()

    if collection is None:
        abort(404)

    if not check_user_id(collection.user_id):
        abort(401)

    try:
        game_id = request.get_json()["game_id"]
        action = request.get_json()["action"]
        if action == "add":
            collection.add(game_id)
        elif action == "remove":
            collection.remove(game_id)
        collection.update()

        return jsonify(
            {
                "success": True,
                "collection_id": collection.id,
                "games_in_collection": collection.games,
                "action": action,
                "game_id": game_id,
            }
        )

    except:
        abort(422)


@main.route("/collections/<int:collection_id>/privacy", methods=["PATCH"])
@requires_auth("patch:collection")
def toggle_collection_privacy(collection_id):
    collection = Collection.query.filter_by(id=collection_id).one_or_none()

    if collection is None:
        abort(404)

    if not check_user_id(collection.user_id):
        abort(401)

    try:
        collection.private = not collection.private
        collection.update()
        return jsonify(
            {
                "success": True,
                "collection_id": collection.id,
                "private": collection.private,
            }
        )

    except:
        abort(422)
