from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.ai_edit import AIEdit
from app.models.user import User
from app.schemas.ai_edit import AIEditSchema

schema = AIEditSchema()


def create_ai_edit_handler():
    payload = request.get_json(silent=True) or {}

    target_table = payload.get("target_table")
    target_id = payload.get("target_id")
    editor_service = payload.get("editor_service")
    user_id = payload.get("user_id")

    if not target_table or target_id is None or not editor_service:
        return jsonify({"error": "target_table, target_id, editor_service are required"}), 400

    if user_id is not None and not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    try:
        row = AIEdit.create(
            target_table=target_table,
            target_id=int(target_id),
            original_content=payload.get("original_content"),
            edited_content=payload.get("edited_content"),
            editor_service=editor_service,
            user=user_id if user_id is not None else None,
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create ai_edit"}), 400

    return jsonify(schema.dump(row)), 201
