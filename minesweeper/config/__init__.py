import os


class BaseConfig(object):
    """
    Base Configuration
    """
    ENV = None
    DEBUG = True
    ERROR_INCLUDE_MESSAGE = False
    JSON_SORT_KEYS = False

    #
    # Database
    #
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = "minesweeper"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}" \
                              f"/{DB_NAME}"


class LocalConfig(BaseConfig):
    ENV = "local"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f"mysql://root:root1234@127.0.0.1/minesweeper"


class DevConfig(BaseConfig):
    ENV = "dev"
    DEBUG = False


ENV = os.environ.get('ENV')
config_class = f"{ENV.title()}Config" if ENV is not None else "BaseConfig"
Config = globals()[config_class]
