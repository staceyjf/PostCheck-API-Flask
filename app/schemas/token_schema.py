from marshmallow import Schema, fields


class TokenSchema(Schema):
    accessToken = fields.Str(required=True)
