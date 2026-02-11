from marshmallow import Schema, fields


class LessonVersionSchema(Schema):
    id = fields.Int(dump_only=True)
    lesson_id = fields.Int(required=True, load_only=True)
    version_number = fields.Int(required=True)
    content_json = fields.Raw(allow_none=True)
    author_id = fields.Int(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
