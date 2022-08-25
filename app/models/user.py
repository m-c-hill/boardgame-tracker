from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app import db

from .collection import Collection
from .crud_model import CRUDModel


class User(db.Model, CRUDModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    auth0_id = Column(String(200), unique=True)
    username = Column(String(50), unique=True)
    email = Column(String(200), unique=True)
    updated_at = Column(DateTime)
    reviews = db.relationship("Review", backref="users", lazy=True)
    collection = db.relationship("Collection", back_populates="user")

    def __init__(self, auth0_id, username, email, updated_at):
        self.auth0_id = auth0_id
        self.username = username
        self.email = email
        self.updated_at = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        # new_collection = Collection(auth0_id)
        # new_collection.add()
        self.collection = Collection(auth0_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        return self.username
