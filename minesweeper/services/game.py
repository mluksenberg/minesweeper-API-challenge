import random

from minesweeper.errors import GameFinishedError, GameCellCoordinatesError, \
    GameCellPerformActionError
from minesweeper.extensions import db
from minesweeper.models.game import Game, Cell, GameStatus, CellStatus
from minesweeper.schema.game import ActionCell


def create_game(mines, width, height):
    game = Game()

    cells = []
    for x in range(width):
        for y in range(height):
            cells.append(
                Cell(game_id=game.game_id,
                     coordinate_x=x,
                     coordinate_y=y,
                     value=0)
            )

    for cell in random.sample(cells, mines):
        cell.has_mine = True
        cell.value = None

    game.cells = cells

    for cell in cells:
        cell.value = len([cell for cell in _get_adjacent_cells(game, cell)
                          if cell.has_mine])

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


def _discover_cell(game, cell):
    cell.status = CellStatus.DISCOVERED
    if cell.has_mine:
        game.status = GameStatus.LOST
    else:
        cells_adjacent = [x for x in _get_adjacent_cells(game, cell)
                          if x.status in
                          [CellStatus.UNKNOWN, CellStatus.QUESTION]]
        if cells_adjacent and not any(
                [cell.has_mine for cell in cells_adjacent]):
            for cell_adjacent in cells_adjacent:
                _discover_cell(game, cell_adjacent)


def _change_cell_status(game, cell, action):
    if action == ActionCell.DISCOVER:
        _discover_cell(game, cell)
    elif action == ActionCell.MARK_FLAG:
        cell.status = CellStatus.FLAG
    elif action == ActionCell.MARK_QUESTION:
        cell.status = CellStatus.QUESTION
    elif action == ActionCell.MARK_UNKNOWN:
        cell.status = CellStatus.UNKNOWN
    game.update(db.session)


def _get_adjacent_cells(game, cell):
    return [x for x in game.cells if _is_adjacent_cell(cell, x)]


def _is_adjacent_cell(cell, target):
    return cell.coordinate_x - 1 <= target.coordinate_x <= cell.coordinate_x + 1 \
           and cell.coordinate_y - 1 <= target.coordinate_y <= cell.coordinate_y + 1 \
           and (target.coordinate_x, target.coordinate_y) != (
               cell.coordinate_x, cell.coordinate_y)


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

    if cell.status == CellStatus.DISCOVERED or \
            (action_cell == ActionCell.DISCOVER and
             cell.status == ActionCell.MARK_FLAG):
        raise GameCellPerformActionError(game.game_id, cell, action_cell)

    _change_cell_status(game, cell, action_cell)

    return game
