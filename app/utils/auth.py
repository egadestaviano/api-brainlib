from flask import request, jsonify
import jwt
from app.models.user import User
from app.models.user_profile import UserProfile
from app.config import SECRET_KEY

def get_user_from_token():
    """Decode JWT dan ambil user + profile"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, None, (jsonify({"error": "Missing or invalid token"}), 401)

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None, None, (jsonify({"error": "Token expired"}), 401)
    except jwt.InvalidTokenError:
        return None, None, (jsonify({"error": "Invalid token"}), 401)

    user = User.get_or_none(User.id == payload.get("user_id"))
    if not user:
        return None, None, (jsonify({"error": "User not found"}), 404)

    profile = (
        getattr(user, 'profile', None)
        if hasattr(user, 'profile') else None
    )

    if hasattr(profile, 'select'):
        profile = profile.first()

    if profile is None:
        profile = UserProfile.get_or_none(UserProfile.user_id == user.id)

    return user, profile, None
