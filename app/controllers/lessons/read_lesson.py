from flask import request, jsonify
from app.models.lesson import Lesson
from app.schemas.lesson import LessonSchema, LessonDetailSchema

list_schema = LessonSchema(many=True)
detail_schema = LessonDetailSchema()


def read_lesson_handler(lesson_id=None):
    if lesson_id is not None:
        row = Lesson.get_or_none(Lesson.id == lesson_id)
        if not row:
            return jsonify({"error": "lesson not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = Lesson.select().order_by(Lesson.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
    })
