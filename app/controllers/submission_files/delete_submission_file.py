from flask import jsonify
from app.models.submission_file import SubmissionFile


def delete_submission_file_handler(pivot_id):
    row = SubmissionFile.get_or_none(SubmissionFile.id == pivot_id)
    if not row:
        return jsonify({"error": "submission_file not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
