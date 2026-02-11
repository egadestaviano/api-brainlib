from marshmallow import Schema, fields

class AIEditSchema(Schema):
    id = fields.Int(dump_only=True)
    target_table = fields.Str(required=True)
    target_id = fields.Int(required=True)
    original_content = fields.Str(allow_none=True)
    edited_content = fields.Str(allow_none=True)
    editor_service = fields.Str(required=True)
    user_id = fields.Int(allow_none=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
