from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

class PostCodeSchema(Schema):
    id = fields.Int(dump_only=True) 
    postcode = fields.Str()
    suburbIds = fields.List(fields.Int())
