from sqlalchemy import Column, Integer, String

from app import db
from .crud_model import CRUDModel


class User(db.Model, CRUDModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    auth0_id = Column(String(200), unique=True)
    username = Column(String(50), unique=True)
    email = Column(String(200), unique=True)
    reviews = db.relationship("Review", backref="users", lazy=True)
    # collection = db.relationship("") # TODO

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        return self.username
