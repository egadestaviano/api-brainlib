from flask import request, jsonify

from app.models.assignment_file import AssignmentFile
from app.models.assignment import Assignment
from app.schemas.assignment_file import AssignmentFileSchema

schema = AssignmentFileSchema()


def update_assignment_file_handler(pivot_id):
    row = AssignmentFile.get_or_none(AssignmentFile.id == pivot_id)
    if not row:
        return jsonify({"error": "assignment_file not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "assignment_id" in payload:
        aid = payload.get("assignment_id")
        if not Assignment.get_or_none(Assignment.id == aid):
            return jsonify({"error": "assignment not found"}), 404
        row.assignment = aid

    if "file_id" in payload:
        try:
            row.file_id = int(payload.get("file_id"))
        except Exception:
            return jsonify({"error": "file_id must be integer"}), 400

    row.save()
    return jsonify(schema.dump(row))
