from flask import jsonify
from app.models.class_membership import ClassMembership


def delete_class_membership_handler(membership_id):
    row = ClassMembership.get_or_none(ClassMembership.id == membership_id)
    if not row:
        return jsonify({"error": "class_membership not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
