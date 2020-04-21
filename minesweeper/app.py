from flask import Flask

import minesweeper.api
import minesweeper.config
import minesweeper.extensions
from minesweeper.errors import HttpError, GameBaseError


def create_app(config: object = minesweeper.config.Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_extensions(app: Flask):
    minesweeper.extensions.marshmallow.init_app(app)
    minesweeper.extensions.db.init_app(app)
    # TODO: Register Sentry or other Crash Analytic app


def register_blueprints(app: Flask):
    @app.route('/health-check')
    def health_check():
        """
        Health check endpoint

        :return: 200
        """
        return {"status": "OK"}

    app.register_blueprint(minesweeper.api.get_blueprint())


def register_errors(app: Flask):
    @app.errorhandler(400)
    @app.errorhandler(422)
    def handle_http_exception(error):
        error_message = error.data.get("messages").get("json")
        return {"code": error.code, "message": error_message}, error.code

    @app.errorhandler(GameBaseError)
    def handle_http_error(error):
        json = {"code": error.code, "message": error.message}
        if minesweeper.config.Config.DEBUG and hasattr(error, "description"):
            json["description"] = error.description
        return json, error.code
