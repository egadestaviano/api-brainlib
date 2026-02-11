from flask import request, jsonify
from app.models.class_membership import ClassMembership


def serialize(row: ClassMembership):
    return {
        "id": row.id,
        "class_id": row.class_ref.id,
        "user_id": row.user.id,
        "role": row.role,
        "is_active": row.is_active,
        "joined_at": row.joined_at.isoformat() if row.joined_at else None,
    }


def read_class_membership_handler(membership_id=None):
    if membership_id is not None:
        row = ClassMembership.get_or_none(ClassMembership.id == membership_id)
        if not row:
            return jsonify({"error": "class_membership not found"}), 404
        return jsonify(serialize(row))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = ClassMembership.select().order_by(ClassMembership.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": [serialize(r) for r in rows],
        "page": page,
        "per_page": per_page,
    })
