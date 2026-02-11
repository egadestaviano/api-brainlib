from flask import jsonify
from app.models.lms_class import LmsClass


def delete_class_handler(class_id):
    row = LmsClass.get_or_none(LmsClass.id == class_id)
    if not row:
        return jsonify({"error": "class not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
