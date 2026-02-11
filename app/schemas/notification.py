from marshmallow import Schema, fields


class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    type = fields.Str(required=True)
    payload = fields.Raw(allow_none=True)
    is_read = fields.Bool(dump_default=False)
    created_at = fields.DateTime(dump_only=True)
