from flask import request, jsonify
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileSchema

list_schema = UserProfileSchema(many=True)
detail_schema = UserProfileSchema()


def read_user_profile_handler(profile_id=None):
    if profile_id is not None:
        profile = UserProfile.get_or_none(UserProfile.id == profile_id)
        if not profile:
            return jsonify({"error": "user_profile not found"}), 404
        return jsonify(detail_schema.dump(profile))

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
    except ValueError:
        page = 1
        per_page = 20
    if per_page > 100:
        per_page = 100

    query = UserProfile.select().order_by(UserProfile.id)
    rows = list(query.paginate(page, per_page))
    return jsonify({
        "data": list_schema.dump(rows),
        "page": page,
        "per_page": per_page,
    })
