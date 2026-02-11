from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.grade import Grade
from app.models.submission import Submission
from app.models.user import User
from app.schemas.grade import GradeSchema

schema = GradeSchema()


def create_grade_handler():
    payload = request.get_json(silent=True) or {}

    submission_id = payload.get("submission_id")
    grader_id = payload.get("grader_id")
    score = payload.get("score")

    if not submission_id or not grader_id or score is None:
        return jsonify({"error": "submission_id, grader_id, score are required"}), 400

    if not Submission.get_or_none(Submission.id == submission_id):
        return jsonify({"error": "submission not found"}), 404
    if not User.get_or_none(User.id == grader_id):
        return jsonify({"error": "grader not found"}), 404

    try:
        row = Grade.create(
            submission=submission_id,
            grader=grader_id,
            score=int(score),
            feedback=payload.get("feedback"),
            graded_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create grade"}), 400

    return jsonify(schema.dump(row)), 201
