import flask
import flask_restplus
import minesweeper.api.game


def get_blueprint() -> flask.Blueprint:
    api_bp = flask.Blueprint("API", __name__, url_prefix="/api")
    api = flask_restplus.Api(api_bp,
                             title="Minesweeper API Challenge",
                             version="0.1.0",
                             description="Minesweeper API v0.1.0")

    api.namespaces = []
    api.add_namespace(minesweeper.api.game.game_ns)

    return api_bp
