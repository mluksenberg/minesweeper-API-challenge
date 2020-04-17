from flask import Flask

import minesweeper.config


def create_app(config: object = minesweeper.config.BaseConfig) -> Flask:
    pass