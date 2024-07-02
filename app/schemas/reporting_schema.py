from marshmallow import Schema, fields


class ReportSchema(Schema):
    class Meta:
        ordered = True
        fields = ("state", "date_sold", "avg_price", "id")
    state = fields.Str(required=False)
    date_sold = fields.Date(required=False)
    avg_price = fields.Int(required=False)
    id = fields.Int(required=False)
