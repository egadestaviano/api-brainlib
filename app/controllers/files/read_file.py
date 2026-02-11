from flask import request, jsonify
from app.models.file import File
from app.schemas.file import FileSchema

list_schema = FileSchema(many=True)
detail_schema = FileSchema()


def read_file_handler(file_id=None):
    if file_id is not None:
        row = File.get_or_none(File.id == file_id)
        if not row:
            return jsonify({"error": "file not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = File.select().order_by(File.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
