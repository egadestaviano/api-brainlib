from flask import request, jsonify
from app.models.lesson_version import LessonVersion
from app.schemas.lesson_version import LessonVersionSchema

schema = LessonVersionSchema()


def update_lesson_version_handler(version_id):
    row = LessonVersion.get_or_none(LessonVersion.id == version_id)
    if not row:
        return jsonify({"error": "lesson_version not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "version_number" in payload:
        row.version_number = payload.get("version_number")
    if "content_json" in payload:
        row.content_json = payload.get("content_json")

    row.save()
    return jsonify(schema.dump(row))
