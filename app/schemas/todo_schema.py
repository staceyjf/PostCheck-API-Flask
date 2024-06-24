from marshmallow import Schema, fields
from marshmallow.validate import Length, Range

class TodoSchema(Schema):
    id = fields.Int(dump_only=True) 
    title = fields.Str(required=True, validate=Length(max=50, error="Title should be smaller than 50 characters"))
    task = fields.Str( validate=Length(max=200, error="Task should be smaller than 200 characters"))
    dueDate = fields.Date(missing=None)
    isCompleted = fields.Bool(missing=False)
    colourId = fields.Int()
    
    # Custom validation on dueDate to ensure its set to the future
    # TASK: consider implications of validating that the date can't be in the past