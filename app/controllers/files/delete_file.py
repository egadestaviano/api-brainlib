from flask import jsonify
from app.models.file import File


def delete_file_handler(file_id):
    row = File.get_or_none(File.id == file_id)
    if not row:
        return jsonify({"error": "file not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
