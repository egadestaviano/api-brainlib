from flask import request, jsonify
from app.models.lesson import Lesson
from app.schemas.lesson import LessonSchema

schema = LessonSchema()


def update_lesson_handler(lesson_id):
    row = Lesson.get_or_none(Lesson.id == lesson_id)
    if not row:
        return jsonify({"error": "lesson not found"}), 404

    payload = request.get_json(silent=True) or {}

    for field in ["title", "summary", "content", "content_json"]:
        if field in payload:
            setattr(row, field, payload.get(field))
    if "is_published" in payload:
        row.is_published = bool(payload.get("is_published"))

    row.save()
    return jsonify(schema.dump(row))
