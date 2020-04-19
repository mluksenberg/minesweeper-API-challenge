

class HttpError(Exception):
    def __init__(self, code, message, description=None):
        self.code = code
        self.message = message
        self.description = description
