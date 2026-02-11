from flask import request, jsonify
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogSchema

list_schema = AuditLogSchema(many=True)
detail_schema = AuditLogSchema()


def read_audit_log_handler(audit_id=None):
    if audit_id is not None:
        row = AuditLog.get_or_none(AuditLog.id == audit_id)
        if not row:
            return jsonify({"error": "audit_log not found"}), 404
        return jsonify(detail_schema.dump(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = AuditLog.select().order_by(AuditLog.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
        "total": query.count(),
    })
