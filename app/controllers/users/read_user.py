from flask import request, jsonify
from app.models.user import User
from app.schemas.user import UserSchema

list_schema = UserSchema(many=True)
detail_schema = UserSchema()


def read_user_handler(user_id=None):
    if user_id is not None:
        user = User.get_or_none(User.id == user_id)
        if not user:
            return jsonify({"error": "user not found"}), 404
        return jsonify(detail_schema.dump(user))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = User.select().order_by(User.id)
    users = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(users),
        "page": page,
        "per_page": per_page,
    })
