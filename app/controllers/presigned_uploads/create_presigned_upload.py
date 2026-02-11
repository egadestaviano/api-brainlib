from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.presigned_upload import PresignedUpload
from app.models.user import User
from app.schemas.presigned_upload import PresignedUploadSchema

schema = PresignedUploadSchema()


def _parse_expires_at(value):
    if value in (None, "", 0):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def create_presigned_upload_handler():
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    key = payload.get("key")
    expires_at_raw = payload.get("expires_at")

    if not user_id or not key or expires_at_raw is None:
        return jsonify({"error": "user_id, key, expires_at are required"}), 400

    if not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    expires_at = _parse_expires_at(expires_at_raw)
    if expires_at is None:
        return jsonify({"error": "expires_at must be ISO datetime"}), 400

    try:
        row = PresignedUpload.create(
            user=user_id,
            key=key,
            mime_type=payload.get("mime_type"),
            filename=payload.get("filename"),
            expires_at=expires_at,
            completed=bool(payload.get("completed", False)),
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "key already exists"}), 409

    return jsonify(schema.dump(row)), 201
