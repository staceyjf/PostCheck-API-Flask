from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from app.schemas.suburb_schema import SuburbSchema

class PostCodeSchema(Schema):
    id = fields.Int(dump_only=True) 
    postcode = fields.Str()
    suburbIds = fields.List(fields.Int(), load_only=True) # Use suburbIds for incoming data
    associatedSuburbs = fields.Nested(SuburbSchema, many=True, dump_only=True) # Supply suburb objects in reponses
