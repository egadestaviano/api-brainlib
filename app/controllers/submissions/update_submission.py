from flask import request, jsonify
from datetime import datetime

from app.models.submission import Submission
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


def update_submission_handler(submission_id):
    row = Submission.get_or_none(Submission.id == submission_id)
    if not row:
        return jsonify({"error": "submission not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "submitted_at" in payload:
        parsed = _parse_submitted_at(payload.get("submitted_at"))
        if payload.get("submitted_at") is not None and parsed is None:
            return jsonify({"error": "submitted_at must be ISO datetime"}), 400
        row.submitted_at = parsed

    if "text_answer" in payload:
        row.text_answer = payload.get("text_answer")

    if "status" in payload:
        row.status = payload.get("status")

    row.save()
    return jsonify(schema.dump(row))
