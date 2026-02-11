from flask import request, jsonify
from app.models.assignment_file import AssignmentFile
from app.schemas.assignment_file import AssignmentFileSchema

list_schema = AssignmentFileSchema(many=True)
detail_schema = AssignmentFileSchema()


def read_assignment_file_handler(pivot_id=None):
    if pivot_id is not None:
        row = AssignmentFile.get_or_none(AssignmentFile.id == pivot_id)
        if not row:
            return jsonify({"error": "assignment_file not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = AssignmentFile.select().order_by(AssignmentFile.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
