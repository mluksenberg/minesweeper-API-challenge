from datetime import datetime
from enum import Enum

from minesweeper.extensions import db


class GameStatus(Enum):
    IN_PROGRESS = 0
    WIN = 1
    LOST = 2


class CellStatus(Enum):
    UNKNOWN = 0
    FLAG = 1
    DISCOVERED = 2
    QUESTION = 3


class Cell(db.Model):
    __tablename__ = "cells"

    cell_id = db.Column("id", db.BigInteger, primary_key=True)
    game_id = db.Column("game_id",
                        db.BigInteger,
                        db.ForeignKey("games.id",
                                      ondelete="CASCADE",
                                      onupdate="CASCADE"),
                        nullable=False)
    status = db.Column("status", db.Enum(CellStatus),
                       nullable=False,
                       default=CellStatus.UNKNOWN)
    value = db.Column("value", db.Integer, nullable=True)
    has_mine = db.Column("has_mine", db.Boolean, nullable=False, default=False)
    coordinate_x = db.Column("x", db.BigInteger, nullable=False)
    coordinate_y = db.Column("y", db.BigInteger, nullable=False)


class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column("id", db.BigInteger, primary_key=True)
    status = db.Column("status", db.Enum(GameStatus), nullable=False,
                       default=GameStatus.IN_PROGRESS)
    datetime = db.Column("datetime", db.BigInteger, nullable=False,
                         default=datetime.utcnow().timestamp())
    cells = db.relationship(Cell, cascade="all, delete-orphan", lazy=True)
