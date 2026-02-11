from flask import jsonify
from app.models.grade import Grade


def delete_grade_handler(grade_id):
    row = Grade.get_or_none(Grade.id == grade_id)
    if not row:
        return jsonify({"error": "grade not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
