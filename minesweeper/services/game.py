import random

from minesweeper.errors import GameFinishedError, GameCellCoordinatesError
from minesweeper.extensions import db
from minesweeper.models.game import Game, Cell, GameStatus, CellStatus
from minesweeper.schema.game import ActionCell


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


def _change_cell_status(game, cell, action):
    if action == ActionCell.DISCOVER:
        cell.status = CellStatus.DISCOVERED
        if cell.has_mine:
            game.status = GameStatus.LOST
    if action == ActionCell.MARK:
        cell.status = CellStatus.FLAG
    game.update(db.session)


def set_cell_action(game_id, coordinate_x, coordinate_y, action_cell):
    game = get_game_by_id(game_id)
    if not game:
        return None

    if game.status != GameStatus.IN_PROGRESS:
        raise GameFinishedError(game_id)

    cells = [cell for cell in game.cells if cell.coordinate_x == coordinate_x
            and cell.coordinate_y == coordinate_y]
    if not cells:
        raise GameCellCoordinatesError(game_id, coordinate_x, coordinate_y)

    cell = cells[0]
    _change_cell_status(game, cell, action_cell)

    return game