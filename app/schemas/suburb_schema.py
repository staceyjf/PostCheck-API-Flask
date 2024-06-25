from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

class SuburbSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str()