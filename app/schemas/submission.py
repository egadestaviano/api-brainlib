from marshmallow import Schema, fields

class SubmissionSchema(Schema):
    id = fields.Int(dump_only=True)
    assignment_id = fields.Int(required=True, load_only=True)
    user_id = fields.Int(required=True, load_only=True)
    submitted_at = fields.DateTime(allow_none=True)
    text_answer = fields.Str(allow_none=True)
    status = fields.Str(dump_default='pending')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
