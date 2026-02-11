from flask import jsonify
from app.models.presigned_upload import PresignedUpload


def delete_presigned_upload_handler(pu_id):
    row = PresignedUpload.get_or_none(PresignedUpload.id == pu_id)
    if not row:
        return jsonify({"error": "presigned_upload not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
