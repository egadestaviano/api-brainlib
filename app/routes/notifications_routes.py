from flask import Blueprint

from app.controllers.notifications.create_notification import create_notification_handler
from app.controllers.notifications.read_notification import read_notification_handler
from app.controllers.notifications.update_notification import update_notification_handler
from app.controllers.notifications.delete_notification import delete_notification_handler


notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@notifications_bp.post("")
def create_notification():
    """
    Create notification
    ---
    tags:
      - Notifications
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - type
          properties:
            user_id:
              type: integer
            type:
              type: string
            payload:
              type: object
            is_read:
              type: boolean
    responses:
      201:
        description: Created
      404:
        description: User not found
    """
    return create_notification_handler()


@notifications_bp.get("")
def list_notifications():
    """
    List notifications
    ---
    tags:
      - Notifications
    parameters:
      - in: query
        name: page
        type: integer
      - in: query
        name: per_page
        type: integer
    responses:
      200:
        description: OK
    """
    return read_notification_handler()


@notifications_bp.get("/<int:notification_id>")
def get_notification(notification_id: int):
    """
    Get notification by id
    ---
    tags:
      - Notifications
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_notification_handler(notification_id=notification_id)


@notifications_bp.put("/<int:notification_id>")
@notifications_bp.patch("/<int:notification_id>")
def update_notification(notification_id: int):
    """
    Update notification
    ---
    tags:
      - Notifications
    consumes:
      - application/json
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            type:
              type: string
            payload:
              type: object
            is_read:
              type: boolean
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_notification_handler(notification_id)


@notifications_bp.delete("/<int:notification_id>")
def delete_notification(notification_id: int):
    """
    Delete notification
    ---
    tags:
      - Notifications
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_notification_handler(notification_id)
