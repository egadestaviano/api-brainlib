from flask import request, jsonify
from app.models.ai_edit import AIEdit
from app.schemas.ai_edit import AIEditSchema

list_schema = AIEditSchema(many=True)
detail_schema = AIEditSchema()


def read_ai_edit_handler(ai_edit_id=None):
    if ai_edit_id is not None:
        row = AIEdit.get_or_none(AIEdit.id == ai_edit_id)
        if not row:
            return jsonify({"error": "ai_edit not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = AIEdit.select().order_by(AIEdit.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
