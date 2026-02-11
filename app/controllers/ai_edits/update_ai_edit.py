from flask import request, jsonify

from app.models.ai_edit import AIEdit
from app.models.user import User
from app.schemas.ai_edit import AIEditSchema

schema = AIEditSchema()


def update_ai_edit_handler(ai_edit_id):
    row = AIEdit.get_or_none(AIEdit.id == ai_edit_id)
    if not row:
        return jsonify({"error": "ai_edit not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "target_table" in payload:
        row.target_table = payload.get("target_table")
    if "target_id" in payload:
        try:
            row.target_id = int(payload.get("target_id"))
        except Exception:
            return jsonify({"error": "target_id must be integer"}), 400
    if "original_content" in payload:
        row.original_content = payload.get("original_content")
    if "edited_content" in payload:
        row.edited_content = payload.get("edited_content")
    if "editor_service" in payload:
        row.editor_service = payload.get("editor_service")
    if "user_id" in payload:
        uid = payload.get("user_id")
        if uid is None:
            row.user = None
        else:
            if not User.get_or_none(User.id == uid):
                return jsonify({"error": "user not found"}), 404
            row.user = uid

    row.save()
    return jsonify(schema.dump(row))
