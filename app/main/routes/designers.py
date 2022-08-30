from flask import abort, jsonify, request

from ...domain.board_game import BoardGame, Designer
from ...utils.auth0 import requires_auth
from ...utils.requests import paginate_items
from .. import main

# from . import GAMES_PER_PAGE
GAMES_PER_PAGE = 10


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
@requires_auth("post:designers")
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

        return (
            jsonify(
                {
                    "success": True,
                    "created": designer.id,
                    "designers": formatted_designers,
                }
            ),
            201,
        )

    except:
        abort(422)


@main.route("/designers/<int:designer_id>", methods=["PATCH"])
@requires_auth("patch:designers")
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
