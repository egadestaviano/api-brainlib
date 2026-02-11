from marshmallow import Schema, fields


class AuditLogSchema(Schema):
    id = fields.Int(dump_only=True)
    actor_id = fields.Int(allow_none=True, load_only=True)
    action = fields.Str(required=True)
    object_type = fields.Str(required=True)
    object_id = fields.Int(allow_none=True)
    details = fields.Raw(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
