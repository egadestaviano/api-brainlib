from flask import request, jsonify
from app.models.presigned_upload import PresignedUpload
from app.schemas.presigned_upload import PresignedUploadSchema

list_schema = PresignedUploadSchema(many=True)
detail_schema = PresignedUploadSchema()


def read_presigned_upload_handler(pu_id=None):
    if pu_id is not None:
        row = PresignedUpload.get_or_none(PresignedUpload.id == pu_id)
        if not row:
            return jsonify({"error": "presigned_upload not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = PresignedUpload.select().order_by(PresignedUpload.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
