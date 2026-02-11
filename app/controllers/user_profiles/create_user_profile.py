from flask import request, jsonify
from peewee import IntegrityError

from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileSchema
from app.models.user import User

schema = UserProfileSchema()


def create_user_profile_handler():
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    display_name = payload.get("display_name")
    avatar_file_id = payload.get("avatar_file_id")
    bio = payload.get("bio")
    extra = payload.get("extra")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    if not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    try:
        profile = UserProfile.create(
            user=user_id,
            display_name=display_name,
            avatar_file_id=avatar_file_id,
            bio=bio,
            extra=extra,
        )
    except IntegrityError:
        return jsonify({"error": "profile already exists for this user"}), 409

    return jsonify(schema.dump(profile)), 201
