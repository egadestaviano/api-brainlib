from flask import jsonify
from app.models.user_profile import UserProfile


def delete_user_profile_handler(profile_id):
    profile = UserProfile.get_or_none(UserProfile.id == profile_id)
    if not profile:
        return jsonify({"error": "user_profile not found"}), 404
    profile.delete_instance(recursive=True)
    return jsonify({"deleted": True})
