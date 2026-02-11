from flask import request, jsonify

from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileSchema

schema = UserProfileSchema()


def update_user_profile_handler(profile_id):
    profile = UserProfile.get_or_none(UserProfile.id == profile_id)
    if not profile:
        return jsonify({"error": "user_profile not found"}), 404

    payload = request.get_json(silent=True) or {}

    for field in ["display_name", "avatar_file_id", "bio", "extra"]:
        if field in payload:
            setattr(profile, field, payload.get(field))

    profile.save()
    return jsonify(schema.dump(profile))
