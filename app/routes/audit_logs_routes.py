from flask import Blueprint

from app.controllers.audit_logs.create_audit_log import create_audit_log_handler
from app.controllers.audit_logs.read_audit_log import read_audit_log_handler
from app.controllers.audit_logs.update_audit_log import update_audit_log_handler
from app.controllers.audit_logs.delete_audit_log import delete_audit_log_handler


audit_logs_bp = Blueprint("audit_logs", __name__, url_prefix="/audit-logs")


@audit_logs_bp.post("")
def create_audit_log():
    """
    Create audit log
    ---
    tags:
      - AuditLogs
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - action
            - object_type
          properties:
            actor_id:
              type: integer
              nullable: true
            action:
              type: string
            object_type:
              type: string
            object_id:
              type: integer
            details:
              type: object
    responses:
      201:
        description: Created
      404:
        description: Actor not found
    """
    return create_audit_log_handler()


@audit_logs_bp.get("")
def list_audit_logs():
    """
    List audit logs
    ---
    tags:
      - AuditLogs
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
    return read_audit_log_handler()


@audit_logs_bp.get("/<int:audit_id>")
def get_audit_log(audit_id: int):
    """
    Get audit log by id
    ---
    tags:
      - AuditLogs
    parameters:
      - in: path
        name: audit_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_audit_log_handler(audit_id=audit_id)


@audit_logs_bp.put("/<int:audit_id>")
@audit_logs_bp.patch("/<int:audit_id>")
def update_audit_log(audit_id: int):
    """
    Update audit log
    ---
    tags:
      - AuditLogs
    consumes:
      - application/json
    parameters:
      - in: path
        name: audit_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            action:
              type: string
            object_type:
              type: string
            object_id:
              type: integer
            details:
              type: object
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_audit_log_handler(audit_id)


@audit_logs_bp.delete("/<int:audit_id>")
def delete_audit_log(audit_id: int):
    """
    Delete audit log
    ---
    tags:
      - AuditLogs
    parameters:
      - in: path
        name: audit_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_audit_log_handler(audit_id)
