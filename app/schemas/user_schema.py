from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta: # To maintain the order as they are defined when being serialized or deserialized
        fields = ("id", "postcode", "suburbIds", "associatedSuburbs")
        ordered = False
        
    id = fields.Int(dump_only=True) 
    public_id = fields.Str()
    username = fields.Str()
    email = fields.Str()
