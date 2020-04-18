

import flask_marshmallow
from flask import Flask

import minesweeper.api
import minesweeper.config


def create_app(config: object = minesweeper.config.Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_extensions(app: Flask):
    flask_marshmallow.Marshmallow().init_app(app)
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

    @app.errorhandler(Exception)
    def handle_unknown_exception(error):
        return {"code": 500, "message": "Internal Server Error"}, 500
