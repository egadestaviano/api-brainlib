from marshmallow import Schema, fields
from app.schemas.user_profile import UserProfileSchema

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    is_active = fields.Bool(dump_default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    profile = fields.Method("get_profile")

    def get_profile(self, obj):
        if obj.profile and len(obj.profile) > 0:
            return UserProfileSchema().dump(obj.profile[0])
        return None
