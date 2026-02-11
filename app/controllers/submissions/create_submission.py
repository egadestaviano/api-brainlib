from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.submission import Submission
from app.models.assignment import Assignment
from app.models.user import User
from app.schemas.submission import SubmissionSchema

schema = SubmissionSchema()


def _parse_submitted_at(value):
    if value in (None, "", 0):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def create_submission_handler():
    payload = request.get_json(silent=True) or {}

    assignment_id = payload.get("assignment_id")
    user_id = payload.get("user_id")

    if not assignment_id or not user_id:
        return jsonify({"error": "assignment_id and user_id are required"}), 400

    if not Assignment.get_or_none(Assignment.id == assignment_id):
        return jsonify({"error": "assignment not found"}), 404
    if not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    submitted_at = _parse_submitted_at(payload.get("submitted_at"))
    if payload.get("submitted_at") is not None and submitted_at is None:
        return jsonify({"error": "submitted_at must be ISO datetime"}), 400

    try:
        row = Submission.create(
            assignment=assignment_id,
            user=user_id,
            submitted_at=submitted_at,
            text_answer=payload.get("text_answer"),
            status=payload.get("status", "pending"),
        )
    except IntegrityError:
        return jsonify({"error": "submission already exists for this assignment/user"}), 409

    return jsonify(schema.dump(row)), 201
