from flask import request, jsonify
from app.models.notification import Notification
from app.schemas.notification import NotificationSchema

list_schema = NotificationSchema(many=True)
detail_schema = NotificationSchema()


def read_notification_handler(notification_id=None):
    if notification_id is not None:
        row = Notification.get_or_none(Notification.id == notification_id)
        if not row:
            return jsonify({"error": "notification not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = Notification.select().order_by(Notification.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
