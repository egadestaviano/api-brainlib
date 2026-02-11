from marshmallow import Schema, fields

class UserProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    display_name = fields.Str(allow_none=True)
    avatar_file_id = fields.Integer(allow_none=True)
    bio = fields.Str(allow_none=True)
    extra = fields.Raw(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
