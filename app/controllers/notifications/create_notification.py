from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime, timezone

from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationSchema

schema = NotificationSchema()


def create_notification_handler():
    payload = request.get_json(silent=True) or {}

    user_id = payload.get("user_id")
    notif_type = payload.get("type")

    if not user_id or not notif_type:
        return jsonify({"error": "user_id and type are required"}), 400

    if not User.get_or_none(User.id == user_id):
        return jsonify({"error": "user not found"}), 404

    try:
        row = Notification.create(
            user=user_id,
            type=notif_type,
            payload=payload.get("payload"),
            is_read=bool(payload.get("is_read", False)),
            created_at=datetime.now(timezone.utc),
        )
    except IntegrityError:
        return jsonify({"error": "failed to create notification"}), 400

    return jsonify(schema.dump(row)), 201
