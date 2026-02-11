from flask import jsonify
from app.models.assignment_file import AssignmentFile


def delete_assignment_file_handler(pivot_id):
    row = AssignmentFile.get_or_none(AssignmentFile.id == pivot_id)
    if not row:
        return jsonify({"error": "assignment_file not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
