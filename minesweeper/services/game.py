import random

from minesweeper.extensions import db
from minesweeper.models.game import Game, Cell


def create_game(mines, width, height):
    game = Game()

    cells = []
    for x in range(width):
        for y in range(height):
            cells.append(
                Cell(game_id=game.game_id, coordinate_x=x, coordinate_y=y)
            )

    for cell in random.sample(cells, mines):
        cell.has_mine = True

    game.cells = cells
    game.save(db.session)
    return game


def get_games(status):
    if status:
        return Game.query.filter(Game.status == status).all()
    return Game.query.all()


def get_game_by_id(game_id):
    return Game.query.filter(Game.game_id == game_id).first()


def delete_game_by_id(game_id):
    game = get_game_by_id(game_id)
    if game:
        game.delete(db.session)
    return game


def discover_cell(game_id, coordinate_x, coordinate_y):
    pass


def _change_cell_status(cell, status):
    pass
