import os
from email.mime import image

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.types import ARRAY

from app import db

# Limits for review ratings
MIN_RATING = 0
MAX_RATING = 5


class CustomModel(db.Model):
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BoardGame(CustomModel):
    __tablename__ = "board_games"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(250))
    min_player_count = Column(Integer)
    max_player_count = Column(Integer)
    play_time = Column(Time)
    release_date = Column(Date)
    age = Column(Integer)
    weight = Column(Float)
    genre = Column(Integer, ForeignKey("genres.id"))
    designer = Column(String(120), ForeignKey("designers.id"))
    publisher = Column(String(120), ForeignKey("publishers.id"))
    image_link = Column(String(2048))
    reviews = db.relationship("Review", backref="games", lazy=True)

    def __init__(
        self,
        title,
        description,
        min_player_count,
        max_player_count,
        play_time,
        release_date,
        age,
        weight,
        genre_id,
        designer_id,
        publisher_id,
        image_link,
    ):
        self.title = title
        self.description = description
        self.min_player_count = min_player_count
        self.max_player_count = max_player_count
        self.play_time = play_time
        self.release_date = release_date
        self.age = age
        self.weight = weight
        self.genre = genre_id
        self.designer = designer_id
        self.publisher = publisher_id
        self.image_link = image_link

    def __repr__(self):
        return f"BoardGame('{self.title}', {self.description})"

    def __str__(self):
        return self.title

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "min_player_count": self.min_player_count,
            "max_player_count": self.max_player_count,
            "play_time": self.play_time,
            "release_date": self.release_date,
            "age": self.age,
            "weight": self.weight,
            "genre": self.genre,
            "designer": self.designer,
            "publisher": self.publisher,
            "image_link": self.image_link,
        }


class Genre(CustomModel):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    description = Column(String(250))
    games = db.relationship("Review", backref="games", lazy=True)

    def __init__(self, name, description, games):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Genre('{self.name}', '{self.description}')"

    def __str__(self):
        return f"{self.name}: {self.description}"


class Designer(CustomModel):
    __tablename__ = "designers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f"Designer('{self.first_name}', '{self.last_name}')"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Publisher(CustomModel):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Publisher('{self.name}')"

    def __str__(self):
        return self.name

    def format(self):
        return {"id": self.id, "name": self.name}


class Review(CustomModel):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    game = Column(Integer, ForeignKey("games.id"))
    review_text = Column(String(1000))
    rating = Column(Integer)  # Rating out of 5 stars
    user = Column(Integer, ForeignKey("users.id"))

    def __init__(self, game_id, review_text, rating, user_id):
        self.game = game_id
        self.review_text = review_text
        self.rating = (
            MIN_RATING
            if rating < MIN_RATING
            else MAX_RATING
            if rating > MAX_RATING
            else rating
        )
        self.user = user_id

    def __repr__(self):
        return f"Review('ID':{self.game}, 'Rating': {self.rating})"

    def __str__(self):
        return f"ID: {self.id}, {self.rating}/5\n{self.review_text}"

    def format(self):
        return {
            "id": self.id,
            "user": self.user,
            "game_id": self.game,
            "rating": self.rating,
            "review_text": self.review_text,
        }


class User(CustomModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(200))
    reviews = db.relationship("Review", backref="users", lazy=True)
    # TODO: implement collection function

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        return self.username
