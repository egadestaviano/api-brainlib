from marshmallow import Schema, fields

class PresignedUploadSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    key = fields.Str(required=True)
    mime_type = fields.Str(allow_none=True)
    filename = fields.Str(allow_none=True)
    expires_at = fields.DateTime(required=True)
    completed = fields.Bool(dump_default=False)
    created_at = fields.DateTime(dump_only=True)
