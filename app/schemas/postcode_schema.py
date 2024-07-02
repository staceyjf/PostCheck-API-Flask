from app.schemas.suburb_schema import SuburbSchema
from marshmallow import Schema, fields


class PostCodeSchema(Schema):
    class Meta:
        fields = ("id", "postcode", "suburbIds", "associatedSuburbs")
        ordered = False
    id = fields.Int()
    postcode = fields.Str()
    suburbIds = fields.List(fields.Int(), load_only=True, required=False)
    associatedSuburbs = fields.Nested(SuburbSchema, many=True, dump_only=True, required=False)
