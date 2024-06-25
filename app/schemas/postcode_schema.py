from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

class PostCodeSchema(Schema):
    id = fields.Int(dump_only=True) 
    postcode = fields.Str(validate=Length(min=4, max=4, error="Postcodes need to be 4 digits long"))
    suburbIds = fields.List(fields.Int())
    
