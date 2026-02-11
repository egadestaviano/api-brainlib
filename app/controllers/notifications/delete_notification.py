from flask import jsonify
from app.models.notification import Notification


def delete_notification_handler(notification_id):
    row = Notification.get_or_none(Notification.id == notification_id)
    if not row:
        return jsonify({"error": "notification not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
