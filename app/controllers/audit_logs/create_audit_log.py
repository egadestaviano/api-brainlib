from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit_log import AuditLogSchema

schema = AuditLogSchema()


def create_audit_log_handler():
    payload = request.get_json(silent=True) or {}

    action = payload.get("action")
    object_type = payload.get("object_type")

    if not action or not object_type:
        return jsonify({"error": "action and object_type are required"}), 400

    actor_id = payload.get("actor_id")
    if actor_id is not None and not User.get_or_none(User.id == actor_id):
        return jsonify({"error": "actor not found"}), 404

    try:
        row = AuditLog.create(
            actor=actor_id if actor_id is not None else None,
            action=action,
            object_type=object_type,
            object_id=payload.get("object_id"),
            details=payload.get("details"),
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create audit_log"}), 400

    return jsonify(schema.dump(row)), 201
