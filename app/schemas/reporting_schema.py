from marshmallow import Schema, fields


class ChartPointSchema(Schema):
    class Meta:
        ordered = True
        fields = ("x", "y")
    y = fields.Float()
    x = fields.Date()


class ReportSchema(Schema):
    class Meta:
        ordered = True
        fields = ("id", "color", "data")
    id = fields.Str()
    color = fields.Str()
    data = fields.List(fields.Nested(ChartPointSchema))
