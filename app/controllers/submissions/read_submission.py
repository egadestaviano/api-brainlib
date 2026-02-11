from flask import request, jsonify
from app.models.submission import Submission
from app.schemas.submission import SubmissionSchema

list_schema = SubmissionSchema(many=True)
detail_schema = SubmissionSchema()


def read_submission_handler(submission_id=None):
    if submission_id is not None:
        row = Submission.get_or_none(Submission.id == submission_id)
        if not row:
            return jsonify({"error": "submission not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = Submission.select().order_by(Submission.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
