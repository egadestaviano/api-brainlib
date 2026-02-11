from flask import request, jsonify
from app.models.submission_file import SubmissionFile
from app.schemas.submission_file import SubmissionFileSchema

list_schema = SubmissionFileSchema(many=True)
detail_schema = SubmissionFileSchema()


def read_submission_file_handler(pivot_id=None):
    if pivot_id is not None:
        row = SubmissionFile.get_or_none(SubmissionFile.id == pivot_id)
        if not row:
            return jsonify({"error": "submission_file not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = SubmissionFile.select().order_by(SubmissionFile.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
