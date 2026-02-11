from flask import request, jsonify
from werkzeug.security import generate_password_hash
from peewee import IntegrityError

from app.models.user import User
from app.schemas.user import UserSchema

schema = UserSchema()


def update_user_handler(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    payload = request.get_json(silent=True) or {}

    new_email = payload.get("email")
    new_password = payload.get("password")
    new_is_active = payload.get("is_active")

    if new_email is not None:
        user.email = new_email
    if new_password is not None:
        user.password_hash = generate_password_hash(new_password)
    if new_is_active is not None:
        user.is_active = bool(new_is_active)

    try:
        user.save()
    except IntegrityError:
        return jsonify({"error": "email already exists"}), 409

    return jsonify(schema.dump(user))
