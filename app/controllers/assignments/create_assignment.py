from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime

from app.models.assignment import Assignment
from app.models.lms_class import LmsClass
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.assignment import AssignmentSchema

schema = AssignmentSchema()


def _parse_due_at(value):
    if value in (None, "", 0):
        return None
    if isinstance(value, datetime):
        return value
    try:
        # Expecting ISO 8601 string
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def create_assignment_handler():
    payload = request.get_json(silent=True) or {}

    class_id = payload.get("class_id")
    title = payload.get("title")
    creator_id = payload.get("creator_id")

    if not class_id or not title or not creator_id:
        return jsonify({"error": "class_id, title, creator_id are required"}), 400

    if not LmsClass.get_or_none(LmsClass.id == class_id):
        return jsonify({"error": "class not found"}), 404
    if not User.get_or_none(User.id == creator_id):
        return jsonify({"error": "creator not found"}), 404

    lesson_id = payload.get("lesson_id")
    if lesson_id is not None:
        if lesson_id != "" and not Lesson.get_or_none(Lesson.id == lesson_id):
            return jsonify({"error": "lesson not found"}), 404

    due_at = _parse_due_at(payload.get("due_at"))
    if payload.get("due_at") is not None and due_at is None:
        return jsonify({"error": "due_at must be ISO datetime"}), 400

    try:
        row = Assignment.create(
            class_ref=class_id,
            lesson=lesson_id if lesson_id not in (None, "") else None,
            title=title,
            description=payload.get("description"),
            instructions=payload.get("instructions"),
            creator=creator_id,
            due_at=due_at,
            allow_file_upload=bool(payload.get("allow_file_upload", False)),
            max_score=int(payload.get("max_score", 100)),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create assignment"}), 400

    return jsonify(schema.dump(row)), 201
