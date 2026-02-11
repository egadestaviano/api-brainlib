from marshmallow import Schema, fields

class SubmissionFileSchema(Schema):
    id = fields.Int(dump_only=True)
    submission_id = fields.Int(required=True, load_only=True)
    file_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
