import os


class BaseConfig(object):
    """
    Base Configuration
    """
    ENV = None
    DEBUG = True
    ERROR_INCLUDE_MESSAGE = False


class LocalConfig(BaseConfig):
    ENV = "local"
    DEBUG = True


class DevConfig(BaseConfig):
    ENV = "dev"
    DEBUG = False


ENV = os.environ.get('ENV')
config_class = f"{ENV.title()}Config" if ENV is not None else "BaseConfig"
Config = globals()[config_class]
