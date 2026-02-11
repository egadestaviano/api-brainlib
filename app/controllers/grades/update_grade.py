from flask import request, jsonify

from app.models.grade import Grade
from app.schemas.grade import GradeSchema

schema = GradeSchema()


def update_grade_handler(grade_id):
    row = Grade.get_or_none(Grade.id == grade_id)
    if not row:
        return jsonify({"error": "grade not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "score" in payload:
        try:
            row.score = int(payload.get("score"))
        except Exception:
            return jsonify({"error": "score must be integer"}), 400
    if "feedback" in payload:
        row.feedback = payload.get("feedback")

    row.save()
    return jsonify(schema.dump(row))
