from marshmallow import Schema, fields


# get ENUM value and not name
class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        # additional Marshmellow args need to be supplied for the serialization method
        if value is None:
            return None
        return value.value


class SuburbSchemaArgs(Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state")
    id = fields.Int(required=False)
    name = fields.Str(required=False)
    state = EnumField(required=False)


class SuburbSchemaBySuburbName(Schema):
    postcode = fields.Str()
