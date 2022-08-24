from enum import unique

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time

from app import db
from .crud_model import CRUDModel


class BoardGame(db.Model, CRUDModel):
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
    genre = Column(Integer, ForeignKey("genres.id"))  # TODO
    designer = Column(Integer, ForeignKey("designers.id"))  # TODO
    publisher = Column(Integer, ForeignKey("publishers.id"))  # TODO
    image_link = Column(String(2048))
    reviews = db.relationship("Review", backref="board_games", lazy=True)  # TODO

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


class Genre(db.Model, CRUDModel):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    description = Column(String(250))
    board_games = db.relationship("BoardGame", backref="genres", lazy=True)  # TODO

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Genre('{self.name}', '{self.description}')"

    def __str__(self):
        return f"{self.name}: {self.description}"

    def format(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Designer(db.Model, CRUDModel):
    __tablename__ = "designers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120))
    last_name = Column(String(120))
    board_games = db.relationship("BoardGame", backref="designers", lazy=True)  # TODO

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


class Publisher(db.Model, CRUDModel):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    board_games = db.relationship("BoardGame", backref="publishers", lazy=True)  # TODO

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Publisher('{self.name}')"

    def __str__(self):
        return self.name

    def format(self):
        return {"id": self.id, "name": self.name}
