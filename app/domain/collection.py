from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.types import ARRAY

from app import db

from ..utils.mutable_list import MutableList
from .crud_model import CRUDModel


class Collection(db.Model, CRUDModel):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    games = Column(
        MutableList.as_mutable(ARRAY(Integer))
    )  # IDs of games in the collection
    private = Column(Boolean, default=True)

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.games = []
        self.private = True

    def __repr__(self) -> str:
        return f"Collection('{self.id}', {self.user_id})"

    def __str__(self) -> str:
        return f"Collection {self.id} contains {len(self.games)} games."

    def add(self, game_id: str) -> None:
        if not self.includes_game(game_id):
            self.games.append(game_id)

    def remove(self, game_id: str) -> None:
        if self.includes_game(game_id):
            self.games.remove(game_id)

    def includes_game(self, game_id) -> bool:
        return game_id in self.games

    def format(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "games": self.games,
            "private": self.private,
        }
