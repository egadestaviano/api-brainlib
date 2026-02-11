from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.submission_file import SubmissionFile
from app.models.submission import Submission
from app.schemas.submission_file import SubmissionFileSchema

schema = SubmissionFileSchema()


def create_submission_file_handler():
    payload = request.get_json(silent=True) or {}

    submission_id = payload.get("submission_id")
    file_id = payload.get("file_id")

    if not submission_id or file_id is None:
        return jsonify({"error": "submission_id and file_id are required"}), 400

    if not Submission.get_or_none(Submission.id == submission_id):
        return jsonify({"error": "submission not found"}), 404

    try:
        row = SubmissionFile.create(
            submission=submission_id,
            file_id=int(file_id),
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "submission-file already exists"}), 409

    return jsonify(schema.dump(row)), 201
