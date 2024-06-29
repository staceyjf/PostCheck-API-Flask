from marshmallow import Schema, fields


class MyBaseSchema(Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "state")


class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value


class SuburbSchema(MyBaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    state = EnumField()
