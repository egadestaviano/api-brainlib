from flask import jsonify
from app.models.submission import Submission


def delete_submission_handler(submission_id):
    row = Submission.get_or_none(Submission.id == submission_id)
    if not row:
        return jsonify({"error": "submission not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
