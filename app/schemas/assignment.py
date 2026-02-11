from marshmallow import Schema, fields


class AssignmentSchema(Schema):
    id = fields.Int(dump_only=True)
    class_id = fields.Int(required=True, load_only=True)
    lesson_id = fields.Int(allow_none=True, load_only=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    instructions = fields.Str(allow_none=True)
    creator_id = fields.Int(required=True, load_only=True)
    due_at = fields.DateTime(allow_none=True)
    allow_file_upload = fields.Bool(dump_default=False)
    max_score = fields.Int(dump_default=100)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
