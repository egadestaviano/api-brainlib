from flask import request, jsonify

from app.models.file import File
from app.schemas.file import FileSchema

schema = FileSchema()


def update_file_handler(file_id):
    row = File.get_or_none(File.id == file_id)
    if not row:
        return jsonify({"error": "file not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "filename" in payload:
        row.filename = payload.get("filename")
    if "mime_type" in payload:
        row.mime_type = payload.get("mime_type")
    if "url" in payload:
        row.url = payload.get("url")
    if "path" in payload:
        row.path = payload.get("path")
    if "size_bytes" in payload:
        try:
            row.size_bytes = int(payload.get("size_bytes"))
        except Exception:
            return jsonify({"error": "size_bytes must be integer"}), 400
    if "purpose" in payload:
        row.purpose = payload.get("purpose")
    if "storage_backend" in payload:
        row.storage_backend = payload.get("storage_backend")
    if "is_public" in payload:
        row.is_public = bool(payload.get("is_public"))
    if "reference_count" in payload:
        try:
            row.reference_count = int(payload.get("reference_count"))
        except Exception:
            return jsonify({"error": "reference_count must be integer"}), 400
    if "metadata" in payload:
        row.metadata = payload.get("metadata")

    row.save()
    return jsonify(schema.dump(row))
