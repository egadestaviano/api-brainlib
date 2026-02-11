from flask import jsonify
from app.models.ai_edit import AIEdit


def delete_ai_edit_handler(ai_edit_id):
    row = AIEdit.get_or_none(AIEdit.id == ai_edit_id)
    if not row:
        return jsonify({"error": "ai_edit not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
