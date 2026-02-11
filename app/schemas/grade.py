from marshmallow import Schema, fields

class GradeSchema(Schema):
    id = fields.Int(dump_only=True)
    submission_id = fields.Int(required=True, load_only=True)
    grader_id = fields.Int(required=True, load_only=True)
    score = fields.Int(required=True)
    feedback = fields.Str(allow_none=True)
    graded_at = fields.DateTime(dump_only=True)
