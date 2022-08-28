from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import ARRAY

from app import db

from .crud_model import CRUDModel

# Limits for review ratings
MIN_RATING = 0
MAX_RATING = 5


class Review(db.Model, CRUDModel):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    board_game = Column(Integer, ForeignKey("board_games.id"))
    review_text = Column(String(1000))
    rating = Column(Integer)  # Rating out of 5 stars
    user = Column(Integer, ForeignKey("users.id"))
    likes = Column(Integer)
    dislikes = Column(Integer)
    _user_likes = Column(ARRAY(Integer))
    _user_dislikes = Column(ARRAY(Integer))

    def __init__(self, game_id, review_text, rating, user_id):
        self.board_game = game_id
        self.review_text = review_text
        self.rating = (
            MIN_RATING
            if rating < MIN_RATING
            else MAX_RATING
            if rating > MAX_RATING
            else rating
        )
        self.user = user_id
        self._user_likes = set([])
        self._user_dislikes = set([])

    @property
    def likes(self) -> int:
        return len(self._user_likes)

    @property
    def dislikes(self) -> int:
        return len(self._user_dislikes)

    def like_review(self, user_id):
        if user_id in self._user_dislikes:
            self._user_dislikes.remove(user_id)
        self._user_likes.add(user_id)

    def dislike_review(self, user_id):
        if user_id in self._user_likes:
            self._user_likes.remove(user_id)
        self._user_dislikes.add(user_id)

    def __repr__(self):
        return f"Review('ID':{self.board_game}, 'Rating': {self.rating})"

    def __str__(self):
        return f"ID: {self.id}, {self.rating}/5\n{self.review_text}"

    def format(self):
        return {
            "id": self.id,
            "user": self.user,
            "game_id": self.board_game,
            "rating": self.rating,
            "review_text": self.review_text,
        }
