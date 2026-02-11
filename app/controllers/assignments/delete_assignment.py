from flask import jsonify
from app.models.assignment import Assignment


def delete_assignment_handler(assignment_id):
    row = Assignment.get_or_none(Assignment.id == assignment_id)
    if not row:
        return jsonify({"error": "assignment not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
