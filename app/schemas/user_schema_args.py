from marshmallow import Schema, fields

class UserSchemaArgs(Schema):
    class Meta: # To maintain the order as they are defined when being serialized or deserialized
        fields = ("username", "email", "password")
        ordered = False
        
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
