from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime

from app.models.user import User
from app.schemas.user import UserSchema
from app.config import SECRET_KEY 

user_schema = UserSchema()

def login_user_handler():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.get_or_none(User.email == email)
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    roles = [ur.role.name for ur in user.roles]
    
    # Demo account logic for students
    if "student" in roles:
        from app.models.class_membership import ClassMembership
        from app.models.lms_class import LmsClass
        
        # Check if student has any classes
        has_classes = ClassMembership.select().where(ClassMembership.user == user.id).exists()
        if not has_classes:
            # Find or create a demo class
            admin_user = User.get_or_none(User.email == "admin@example.com")
            if admin_user:
                now = datetime.datetime.utcnow()
                demo_class, _ = LmsClass.get_or_create(
                    code="DEMO123",
                    defaults={
                        "title": "Introduction to Mentora (Demo)",
                        "description": "This is a demo class to help you get started.",
                        "creator": admin_user,
                        "visibility": "public",
                        "created_at": now,
                        "updated_at": now
                    }
                )
                
                # Enroll user
                ClassMembership.get_or_create(
                    class_ref=demo_class,
                    user=user,
                    defaults={
                        "role": "student",
                        "joined_at": now,
                        "is_active": True
                    }
                )

    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "roles": roles,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "type": "Bearer",
        "token": token,
    }), 200
