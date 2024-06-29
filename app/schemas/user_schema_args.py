from marshmallow import Schema, fields


class UserSchemaArgs(Schema):
    class Meta:
        fields = ("username", "email", "password")
        ordered = False
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
