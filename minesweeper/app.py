from flask import Flask

import minesweeper.config


def create_app(config: object = minesweeper.config.Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Flask):
    pass


def register_blueprints(app: Flask):
    @app.route('/health-check')
    def health_check():
        """
        Health check endpoint

        :return: 200
        """
        return {"status": "OK"}