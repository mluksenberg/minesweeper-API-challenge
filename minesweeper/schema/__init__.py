import json

import flask_restplus
from marshmallow import ValidationError
from webargs.flaskparser import parser

from minesweeper.errors import HttpError


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    code = error_status_code if error_status_code else 500
    code = 400 if isinstance(error, ValidationError) else code
    message = str(error.messages) \
        if error.messages else "Internal Server Error"
    raise HttpError(code=code, message=message)
