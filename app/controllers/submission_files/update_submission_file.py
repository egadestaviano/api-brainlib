from flask import request, jsonify

from app.models.submission_file import SubmissionFile
from app.models.submission import Submission
from app.schemas.submission_file import SubmissionFileSchema

schema = SubmissionFileSchema()


def update_submission_file_handler(pivot_id):
    row = SubmissionFile.get_or_none(SubmissionFile.id == pivot_id)
    if not row:
        return jsonify({"error": "submission_file not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "submission_id" in payload:
        sid = payload.get("submission_id")
        if not Submission.get_or_none(Submission.id == sid):
            return jsonify({"error": "submission not found"}), 404
        row.submission = sid

    if "file_id" in payload:
        try:
            row.file_id = int(payload.get("file_id"))
        except Exception:
            return jsonify({"error": "file_id must be integer"}), 400

    row.save()
    return jsonify(schema.dump(row))
