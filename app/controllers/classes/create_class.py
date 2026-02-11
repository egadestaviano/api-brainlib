from flask import request, jsonify
from app.models.lms_class import LmsClass
from app.models.user_profile import UserProfile
from app.schemas.lms_class import ClassCreateSchema, ClassListSchema
from app.utils.auth import get_user_from_token
from peewee import IntegrityError
import random, string

create_schema = ClassCreateSchema()
list_schema = ClassListSchema()

def generate_class_code(length=8):
    """Generate kode unik untuk kelas"""
    chars = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        exists = LmsClass.select().where(LmsClass.code == code).exists()
        if not exists:
            return code


def create_class_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

    json_data = request.get_json() or {}
    errors = create_schema.validate(json_data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        new_class = LmsClass.create(
            title=json_data["title"],
            description=json_data.get("description"),
            creator=user,
            visibility="private",
            code=generate_class_code()
        )

        try:
            creator_profile = UserProfile.get(UserProfile.user == user.id)
            setattr(new_class.creator, "profile", [creator_profile])
        except UserProfile.DoesNotExist:
            setattr(new_class.creator, "profile", [])

        setattr(new_class, "member_count", 0)

        return jsonify({
            "message": "Class created successfully",
            "data": list_schema.dump(new_class)
        }), 201

    except IntegrityError as e:
        return jsonify({
            "error": "Failed to create class",
            "details": str(e)
        }), 500
