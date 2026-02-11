from flask import request, jsonify
from app.models.class_membership import ClassMembership


def update_class_membership_handler(membership_id):
    row = ClassMembership.get_or_none(ClassMembership.id == membership_id)
    if not row:
        return jsonify({"error": "class_membership not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "role" in payload:
        row.role = payload.get("role")
    if "is_active" in payload:
        row.is_active = bool(payload.get("is_active"))

    row.save()
    return jsonify({
        "id": row.id,
        "class_id": row.class_ref.id,
        "user_id": row.user.id,
        "role": row.role,
        "is_active": row.is_active,
        "joined_at": row.joined_at.isoformat() if row.joined_at else None,
    })
