from marshmallow import Schema, fields, validates_schema, ValidationError


class GamePostRequestSchema(Schema):
    mines = fields.Integer(required=True, validate=lambda x: x > 0)
    width = fields.Integer(required=True, validate=lambda x: x > 0)
    height = fields.Integer(required=True, validate=lambda x: x > 0)

    @validates_schema
    def validate_mines(self, data, **kwargs):
        if data["mines"] >= data["width"] + data["height"]:
            raise ValidationError("There are more or equals mines than cells")
