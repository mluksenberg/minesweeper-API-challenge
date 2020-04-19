import random

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
    game.save()
    return game


def discover_cell(game_id, coordinate_x, coordinate_y):
    pass


def _change_cell_status(cell, status):
    pass
