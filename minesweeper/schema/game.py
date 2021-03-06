from enum import Enum

from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow_enum import EnumField

import minesweeper.models.game


class ActionCell(Enum):
    DISCOVER = 0
    MARK_FLAG = 1
    MARK_QUESTION = 2
    MARK_UNKNOWN = 3


class GameBaseSchema(Schema):
    class Meta:
        ordered = True


class GamePutRequestSchema(GameBaseSchema):
    action = EnumField(ActionCell, required=True)
    coordinate_x = fields.Integer(required=True, validate=lambda x: x >= 0)
    coordinate_y = fields.Integer(required=True, validate=lambda x: x >= 0)


class GameListPostRequestSchema(GameBaseSchema):
    mines = fields.Integer(required=True, validate=lambda x: x > 0)
    width = fields.Integer(required=True, validate=lambda x: x > 0)
    height = fields.Integer(required=True, validate=lambda x: x > 0)

    @validates_schema
    def validate_mines(self, data, **kwargs):
        if data["mines"] >= data["width"] * data["height"]:
            raise ValidationError("There are more or equals mines than cells")


class GameListGetRequestSchema(GameBaseSchema):
    status = EnumField(minesweeper.models.game.GameStatus,
                       required=False,
                       missing=None,
                       dump_by=EnumField.VALUE)


class CellModelSchema(GameBaseSchema):
    id = fields.Integer(attribute="cell_id")
    status = EnumField(minesweeper.models.game.CellStatus)
    value = fields.Integer()
    has_mine = fields.Boolean()
    coordinate_x = fields.Integer()
    coordinate_y = fields.Integer()


class GameModelSchema(GameBaseSchema):
    id = fields.Integer(attribute="game_id")
    status = EnumField(minesweeper.models.game.GameStatus)
    datetime = fields.Integer()
    board = fields.Nested(CellModelSchema, many=True, attribute="cells")
