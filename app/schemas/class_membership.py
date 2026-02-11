from marshmallow import Schema, fields

class ClassMembershipSchema(Schema):
    id = fields.Int(dump_only=True)
    class_id = fields.Int(required=True, load_only=True)
    user_id = fields.Int(required=True, load_only=True)
    role = fields.Str(dump_default='member')
    joined_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_default=True)
