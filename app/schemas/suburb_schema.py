from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

 # To ensure we are getting the name rather than the string representation of the ENUM
class MyBaseSchema(Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state")
        
class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs): # additional Marshmellow args need to be supplied for the serialization method
        if value is None:
            return None
        return value.value 

class SuburbSchema(MyBaseSchema):
    # class Meta: # To maintain the order as they are defined when being serialized or deserialized
    #     fields = ("id", "name", "state")
    #     ordered = False
        
    id = fields.Int(dump_only=True) 
    name = fields.Str()
    state = EnumField()

