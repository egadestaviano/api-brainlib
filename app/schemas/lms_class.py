from marshmallow import Schema, fields, validate
from app.schemas.user import UserSchema
from app.schemas.lesson import LessonSchema


class ClassMembershipSchema(Schema):
    id = fields.Int(dump_only=True)
    role = fields.Str()
    joined_at = fields.DateTime()
    is_active = fields.Bool()
    user = fields.Nested(UserSchema, dump_only=True)


class ClassListSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    code = fields.Str(required=True)
    visibility = fields.Str(dump_default="private")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    creator = fields.Nested(UserSchema, dump_only=True)
    member_count = fields.Int()


class ClassDetailSchema(ClassListSchema):
    memberships = fields.List(fields.Nested(ClassMembershipSchema))
    lessons = fields.List(fields.Nested(LessonSchema))


class ClassCreateSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Title is required")
    )
    description = fields.Str(allow_none=True)

class ClassUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1))
    description = fields.Str(allow_none=True)
    visibility = fields.Str(validate=validate.OneOf(["private", "public"]))
