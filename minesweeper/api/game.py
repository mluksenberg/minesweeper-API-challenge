import logging

import flask_restplus
import webargs.flaskparser

from minesweeper.errors import HttpError
from minesweeper.models.game import CellStatus
from minesweeper.schema.game import GameListPostRequestSchema, GameModelSchema, \
    GameListGetRequestSchema, GamePutRequestSchema
from minesweeper.services.game import create_game, get_games, get_game_by_id, \
    delete_game_by_id, set_cell_action

logger = logging.getLogger(__name__)

game_ns = flask_restplus.Namespace("game", description="Game endpoints")


@game_ns.route("/<int:game_id>")
class Game(flask_restplus.Resource):

    @staticmethod
    def get(game_id):
        game = get_game_by_id(game_id)
        if not game:
            raise HttpError(code=404,
                            message=f"Game with ID {game_id} not found")
        return GameModelSchema().dump(game)

    @staticmethod
    def delete(game_id):
        game = delete_game_by_id(game_id)
        if not game:
            raise HttpError(code=404,
                            message=f"Game with ID {game_id} not found")
        return GameModelSchema().dump(game)

    @staticmethod
    @webargs.flaskparser.use_kwargs(GamePutRequestSchema())
    def put(game_id, action, coordinate_x, coordinate_y):
        game = set_cell_action(game_id, coordinate_x, coordinate_y, action)
        if not game:
            raise HttpError(code=404,
                            message=f"Game with ID {game_id} not found")
        return GameModelSchema().dump(game)


@game_ns.route("")
class GameList(flask_restplus.Resource):

    @staticmethod
    @webargs.flaskparser.use_kwargs(GameListGetRequestSchema(),
                                    location="query")
    def get(status):
        logger.info("Get all games")
        games = get_games(status)
        return GameModelSchema().dump(games, many=True)

    @staticmethod
    @webargs.flaskparser.use_kwargs(GameListPostRequestSchema())
    def post(mines, width, height):
        logger.info("Creating Game")
        game = create_game(mines, width, height)
        return GameModelSchema().dump(game)
