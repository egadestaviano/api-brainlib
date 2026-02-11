from flask import request, jsonify
from datetime import datetime

from app.models.presigned_upload import PresignedUpload
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


def update_presigned_upload_handler(pu_id):
    row = PresignedUpload.get_or_none(PresignedUpload.id == pu_id)
    if not row:
        return jsonify({"error": "presigned_upload not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "key" in payload:
        row.key = payload.get("key")
    if "mime_type" in payload:
        row.mime_type = payload.get("mime_type")
    if "filename" in payload:
        row.filename = payload.get("filename")
    if "expires_at" in payload:
        parsed = _parse_expires_at(payload.get("expires_at"))
        if parsed is None and payload.get("expires_at") is not None:
            return jsonify({"error": "expires_at must be ISO datetime"}), 400
        row.expires_at = parsed
    if "completed" in payload:
        row.completed = bool(payload.get("completed"))

    row.save()
    return jsonify(schema.dump(row))
