from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.file import File
from app.models.user import User
from app.schemas.file import FileSchema

schema = FileSchema()


def create_file_handler():
    payload = request.get_json(silent=True) or {}

    owner_id = payload.get("owner_id")
    filename = payload.get("filename")

    if not owner_id or not filename:
        return jsonify({"error": "owner_id and filename are required"}), 400

    if not User.get_or_none(User.id == owner_id):
        return jsonify({"error": "owner not found"}), 404

    try:
        row = File.create(
            owner=owner_id,
            filename=filename,
            mime_type=payload.get("mime_type"),
            url=payload.get("url"),
            path=payload.get("path"),
            size_bytes=int(payload.get("size_bytes", 0)),
            purpose=payload.get("purpose"),
            storage_backend=payload.get("storage_backend", "local"),
            is_public=bool(payload.get("is_public", False)),
            reference_count=int(payload.get("reference_count", 0)),
            metadata=payload.get("metadata"),
            uploaded_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create file"}), 400

    return jsonify(schema.dump(row)), 201
