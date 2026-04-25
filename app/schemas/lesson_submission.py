from marshmallow import Schema, fields, post_load
from app.models.lesson_submission import LessonSubmission

class LessonSubmissionSchema(Schema):
    id = fields.Int(dump_only=True)
    lesson_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    answers_json = fields.Str()
    submitted_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
