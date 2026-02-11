from flask import jsonify
from app.models.audit_log import AuditLog


def delete_audit_log_handler(audit_id):
    row = AuditLog.get_or_none(AuditLog.id == audit_id)
    if not row:
        return jsonify({"error": "audit_log not found"}), 404
    row.delete_instance(recursive=True)
    return jsonify({"deleted": True})
