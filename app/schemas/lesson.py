from marshmallow import Schema, fields

class LessonSchema(Schema):
    id = fields.Int(dump_only=True)
    class_id = fields.Int(required=True, load_only=True)
    title = fields.Str(required=True)
    summary = fields.Str(allow_none=True)
    author_id = fields.Int(required=True, load_only=True)
    is_published = fields.Bool(dump_default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class LessonDetailSchema(LessonSchema):
    content = fields.Str(allow_none=True)
    content_json = fields.Raw(allow_none=True)
    