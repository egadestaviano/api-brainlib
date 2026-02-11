from flask import request, jsonify
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentSchema

list_schema = AssignmentSchema(many=True)
detail_schema = AssignmentSchema()


def read_assignment_handler(assignment_id=None):
    if assignment_id is not None:
        row = Assignment.get_or_none(Assignment.id == assignment_id)
        if not row:
            return jsonify({"error": "assignment not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = Assignment.select().order_by(Assignment.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
