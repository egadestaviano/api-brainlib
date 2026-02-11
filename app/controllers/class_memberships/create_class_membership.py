from flask import request, jsonify
from peewee import IntegrityError

from app.models.class_membership import ClassMembership
from app.models.lms_class import LmsClass
from app.models.user import User


def create_class_membership_handler():
    payload = request.get_json(silent=True) or {}

    class_id = payload.get("class_id")
    user_id = payload.get("user_id")
    role = payload.get("role", "member")
    is_active = payload.get("is_active", True)

    if not class_id or not user_id:
        return jsonify({"error": "class_id and user_id are required"}), 400

    if not LmsClass.get_or_none(LmsClass.id == class_id):
        return jsonify({"error": "class not found"}), 404
    if not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    try:
        row = ClassMembership.create(
            class_ref=class_id,
            user=user_id,
            role=role,
            is_active=bool(is_active),
        )
    except IntegrityError:
        return jsonify({"error": "membership already exists"}), 409

    return jsonify({
        "id": row.id,
        "class_id": row.class_ref.id,
        "user_id": row.user.id,
        "role": row.role,
        "is_active": row.is_active,
        "joined_at": row.joined_at.isoformat() if row.joined_at else None,
    }), 201
