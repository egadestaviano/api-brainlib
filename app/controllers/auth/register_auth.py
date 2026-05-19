import jwt
import datetime
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from peewee import IntegrityError

from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user import UserSchema
from app.config import SECRET_KEY

user_schema = UserSchema()

def register_user_handler():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    password = payload.get("password")
    is_active = payload.get("is_active", True)
    display_name = payload.get("display_name")
    role_name = payload.get("role", "student").lower()

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if role_name not in ["student", "teacher"]:
        role_name = "student"

    try:
        user = User.create(
            email=email,
            password_hash=generate_password_hash(password),
            is_active=bool(is_active),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        
        # Optionally create a UserProfile
        if display_name:
            UserProfile.create(
                user=user,
                display_name=display_name,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            
        # Create UserRole entry
        from app.models.user import Role, UserRole
        role_obj, _ = Role.get_or_create(
            name=role_name,
            defaults={"description": f"{role_name.capitalize()} role"}
        )
        UserRole.create(user=user, role=role_obj)
            
    except IntegrityError:
        return jsonify({"error": "email already exists"}), 409

    # Generate token
    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "roles": [role_name],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "type": "Bearer",
        "token": token,
    }), 201
