from flask import request, jsonify

from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogSchema

schema = AuditLogSchema()


def update_audit_log_handler(audit_id):
    row = AuditLog.get_or_none(AuditLog.id == audit_id)
    if not row:
        return jsonify({"error": "audit_log not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "action" in payload:
        row.action = payload.get("action")
    if "object_type" in payload:
        row.object_type = payload.get("object_type")
    if "object_id" in payload:
        row.object_id = payload.get("object_id")
    if "details" in payload:
        row.details = payload.get("details")

    row.save()
    return jsonify(schema.dump(row))
