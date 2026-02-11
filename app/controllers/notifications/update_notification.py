from flask import request, jsonify

from app.models.notification import Notification
from app.schemas.notification import NotificationSchema

schema = NotificationSchema()


def update_notification_handler(notification_id):
    row = Notification.get_or_none(Notification.id == notification_id)
    if not row:
        return jsonify({"error": "notification not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "type" in payload:
        row.type = payload.get("type")
    if "payload" in payload:
        row.payload = payload.get("payload")
    if "is_read" in payload:
        row.is_read = bool(payload.get("is_read"))

    row.save()
    return jsonify(schema.dump(row))
