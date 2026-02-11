from flask import jsonify
from app.models.user import User


def delete_user_handler(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    user.delete_instance(recursive=True)
    return jsonify({"deleted": True})
