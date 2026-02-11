from flask import request, jsonify
from app.models.lesson_version import LessonVersion
from app.schemas.lesson_version import LessonVersionSchema

list_schema = LessonVersionSchema(many=True)
detail_schema = LessonVersionSchema()


def read_lesson_version_handler(version_id=None):
    if version_id is not None:
        row = LessonVersion.get_or_none(LessonVersion.id == version_id)
        if not row:
            return jsonify({"error": "lesson_version not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = LessonVersion.select().order_by(LessonVersion.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
    })
