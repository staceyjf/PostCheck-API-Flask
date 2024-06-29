from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        fields = ("id", "username", "email")
        ordered = False
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
