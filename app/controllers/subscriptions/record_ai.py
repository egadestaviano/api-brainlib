from flask import jsonify
from app.utils.auth import get_user_from_token
from app.utils.subscription_limits import check_ai_limit, record_ai_usage

def record_ai_usage_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

    # Check limit
    allowed, response_error, status_code = check_ai_limit(user.id)
    if not allowed:
        return response_error, status_code

    # Record usage
    record_ai_usage(user.id)

    return jsonify({"success": True, "message": "AI usage recorded"}), 200
