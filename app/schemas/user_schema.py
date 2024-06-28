from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta: # To maintain the order as they are defined when being serialized or deserialized
        fields = ("id", "username", "email")
        ordered = False
        
    id = fields.Int(dump_only=True) 
    username = fields.Str()
    email = fields.Str()
