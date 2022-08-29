from flask import Blueprint

main = Blueprint("main", __name__)

from .routes import (
    board_games,
    collections,
    designers,
    docs,
    genres,
    publishers,
    reviews,
    search,
    users,
)
