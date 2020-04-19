import logging

import flask_restplus
import webargs.flaskparser

from minesweeper.schema.game import GamePostRequestSchema, GameModelSchema
from minesweeper.services.game import create_game

logger = logging.getLogger(__name__)

game_ns = flask_restplus.Namespace("game", description="Game endpoints")


@game_ns.route("")
class GameList(flask_restplus.Resource):

    @staticmethod
    def get():
        logger.info("Get all games")
        return [{"test": "response"}]

    @staticmethod
    @webargs.flaskparser.use_kwargs(GamePostRequestSchema())
    def post(mines, width, height):
        logger.info("Creating Game")
        game = create_game(mines, width, height)
        return GameModelSchema().dump(game)
