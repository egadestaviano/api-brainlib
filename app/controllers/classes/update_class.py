from flask import request, jsonify
from peewee import IntegrityError

from app.models.lms_class import LmsClass
from app.schemas.lms_class import ClassListSchema

schema = ClassListSchema()


def update_class_handler(class_id):
    row = LmsClass.get_or_none(LmsClass.id == class_id)
    if not row:
        return jsonify({"error": "class not found"}), 404

    payload = request.get_json(silent=True) or {}

    for field in ["title", "description", "visibility"]:
        if field in payload:
            setattr(row, field, payload.get(field))
    if "code" in payload:
        row.code = payload.get("code")

    try:
        row.save()
    except IntegrityError:
        return jsonify({"error": "code already exists"}), 409

    return jsonify(schema.dump(row))
