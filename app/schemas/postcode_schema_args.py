from marshmallow import Schema, fields
# from app.schemas.suburb_schema import SuburbSchema


class PostCodeSchemaArgs(Schema):
    class Meta:
        fields = ("postcode", "suburbIds")
        ordered = False
    postcode = fields.Str()
    suburbIds = fields.List(fields.Int(), load_only=True, required=False)
    # Use suburbIds for incoming data
    # associatedSuburbs = fields.Nested(SuburbSchema, many=True, dump_only=True, required=False)
    # Supply suburb objects in reponses


class PostCodeSchemaBySuburbName(Schema):
    class Meta:
        # To maintain the order as they are defined when being serialized or deserialized
        fields = ("postcode", "suburb")
        ordered = False
    postcode = fields.Str(required=False)
    suburb = fields.Str(required=False)
