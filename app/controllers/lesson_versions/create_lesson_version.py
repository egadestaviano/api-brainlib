from flask import request, jsonify
from peewee import IntegrityError

from app.models.lesson_version import LessonVersion
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.lesson_version import LessonVersionSchema

schema = LessonVersionSchema()


def create_lesson_version_handler():
    payload = request.get_json(silent=True) or {}

    lesson_id = payload.get("lesson_id")
    version_number = payload.get("version_number")
    author_id = payload.get("author_id")
    content_json = payload.get("content_json")

    if not lesson_id or version_number is None or not author_id:
        return jsonify({"error": "lesson_id, version_number, author_id are required"}), 400

    if not Lesson.get_or_none(Lesson.id == lesson_id):
        return jsonify({"error": "lesson not found"}), 404
    if not User.get_or_none(User.id == author_id):
        return jsonify({"error": "author not found"}), 404

    try:
        row = LessonVersion.create(
            lesson=lesson_id,
            version_number=version_number,
            author=author_id,
            content_json=content_json,
        )
    except IntegrityError:
        return jsonify({"error": "version already exists for this lesson"}), 409

    return jsonify(schema.dump(row)), 201
