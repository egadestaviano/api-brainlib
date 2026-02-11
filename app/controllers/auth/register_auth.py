from flask import request, jsonify
from werkzeug.security import generate_password_hash
from peewee import IntegrityError

from app.models.user import User
from app.schemas.user import UserSchema

user_schema = UserSchema()

def register_user_handler():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    password = payload.get("password")
    is_active = payload.get("is_active", True)

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    try:
        user = User.create(
            email=email,
            password_hash=generate_password_hash(password),
            is_active=bool(is_active),
        )
    except IntegrityError:
        return jsonify({"error": "email already exists"}), 409

    return jsonify(user_schema.dump(user)), 201
