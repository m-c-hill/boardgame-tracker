from flask import jsonify, request

from ...models.board_game import BoardGame
from .. import main


@main.route("/search", methods=["POST"])
def search_games():
    search_term = request.get_json().get("search_term", "")

    search_results = BoardGame.query.filter(
        BoardGame.title.ilike(f"%{search_term}%")
    ).all()
    games = [game.format() for game in search_results]

    return jsonify(
        {
            "success": True,
            "search_term": search_term,
            "games": games,
            "total_games": len(games),
        }
    )
