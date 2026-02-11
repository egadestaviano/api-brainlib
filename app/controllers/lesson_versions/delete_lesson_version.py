from flask import jsonify
from app.models.lesson_version import LessonVersion


def delete_lesson_version_handler(version_id):
    row = LessonVersion.get_or_none(LessonVersion.id == version_id)
    if not row:
        return jsonify({"error": "lesson_version not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
