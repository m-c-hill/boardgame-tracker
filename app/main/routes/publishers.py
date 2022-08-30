from flask import abort, jsonify, request

from ...domain.board_game import BoardGame, Publisher
from ...utils.auth0 import requires_auth
from ...utils.requests import paginate_items
from .. import main
from . import GAMES_PER_PAGE


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
@requires_auth("post:publishers")
def create_publisher():
    body = request.get_json()

    try:
        publisher = Publisher(name=body.get("name"))
        publisher.insert()

        publishers = Publisher.query.order_by(Publisher.id).all()
        formatted_publishers = {
            publisher.id: publisher.name for publisher in publishers
        }

        return (
            jsonify(
                {
                    "success": True,
                    "created": publisher.id,
                    "publishers": formatted_publishers,
                }
            ),
            201,
        )

    except:
        abort(422)


@main.route("/publishers/<int:publisher_id>", methods=["PATCH"])
@requires_auth("patch:publishers")
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

        return (
            jsonify(
                {
                    "success": True,
                    "updated": publisher.id,
                    "publishers": formatted_publishers,
                }
            ),
            201,
        )
    except:
        abort(422)
