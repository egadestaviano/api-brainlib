from flask import jsonify
from app.models.lesson import Lesson


def delete_lesson_handler(lesson_id):
    row = Lesson.get_or_none(Lesson.id == lesson_id)
    if not row:
        return jsonify({"error": "lesson not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
