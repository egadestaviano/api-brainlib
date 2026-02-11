from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.assignment_file import AssignmentFile
from app.models.assignment import Assignment
from app.schemas.assignment_file import AssignmentFileSchema

schema = AssignmentFileSchema()


def create_assignment_file_handler():
    payload = request.get_json(silent=True) or {}

    assignment_id = payload.get("assignment_id")
    file_id = payload.get("file_id")

    if not assignment_id or file_id is None:
        return jsonify({"error": "assignment_id and file_id are required"}), 400

    if not Assignment.get_or_none(Assignment.id == assignment_id):
        return jsonify({"error": "assignment not found"}), 404

    try:
        row = AssignmentFile.create(
            assignment=assignment_id,
            file_id=int(file_id),
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "assignment-file already exists"}), 409

    return jsonify(schema.dump(row)), 201
