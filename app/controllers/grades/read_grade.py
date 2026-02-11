from flask import request, jsonify
from app.models.grade import Grade
from app.schemas.grade import GradeSchema

list_schema = GradeSchema(many=True)
detail_schema = GradeSchema()


def read_grade_handler(grade_id=None):
    if grade_id is not None:
        row = Grade.get_or_none(Grade.id == grade_id)
        if not row:
            return jsonify({"error": "grade not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = Grade.select().order_by(Grade.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
