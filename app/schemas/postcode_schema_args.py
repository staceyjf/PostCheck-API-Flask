from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from app.schemas.suburb_schema import SuburbSchema

class PostCodeSchemaArgs(Schema):
    class Meta: # To maintain the order as they are defined when being serialized or deserialized
        fields = ("id", "postcode", "suburbIds", "associatedSuburbs")
        ordered = False
        
    id = fields.Int(dump_only=True) 
    postcode = fields.Str()
    suburbIds = fields.List(fields.Int(), load_only=True, required=False) # Use suburbIds for incoming data
    associatedSuburbs = fields.Nested(SuburbSchema, many=True, dump_only=True, required=False) # Supply suburb objects in reponses
