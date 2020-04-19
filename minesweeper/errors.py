class GameBaseError(Exception):
    pass


class HttpError(GameBaseError):
    def __init__(self, code, message, description=None):
        self.code = code
        self.message = message
        self.description = description


class GameFinishedError(GameBaseError):
    def __init__(self, game_id):
        self.code = 400
        self.message = f"Game with ID {game_id} is finished"


class GameCellCoordinatesError(GameBaseError):
    def __init__(self, game_id, coordinate_x, coordinate_y):
        self.code = 400
        self.message = f"Game ID {game_id} doesn't have the coordinates " \
                       f"({coordinate_x},{coordinate_y})"
