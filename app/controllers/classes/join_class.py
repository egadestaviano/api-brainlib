from flask import request, jsonify
from peewee import IntegrityError
from app.models.lms_class import LmsClass
from app.models.class_membership import ClassMembership
from app.utils.auth import get_user_from_token

def join_class_by_code_handler():
    """
    Endpoint: POST /api/classes/join
    Body: { "code": "ABCDEFGH" }
    """
    user, profile, error = get_user_from_token()
    if error:
        return error 

    payload = request.get_json(silent=True) or {}
    code = payload.get("code")

    if not code:
        return jsonify({"error": "Class code is required"}), 400

    lms_class = LmsClass.get_or_none(LmsClass.code == code)
    if not lms_class:
        return jsonify({"error": "Invalid class code"}), 404
    
    if lms_class.creator.id == user.id:
        return jsonify({"error": "Creator cannot join their own class"}), 403    

    existing = ClassMembership.get_or_none(
        (ClassMembership.class_ref == lms_class.id) &
        (ClassMembership.user == user.id)
    )
    if existing:
        return jsonify({"error": "You are already a member of this class"}), 409

    try:
        membership = ClassMembership.create(
            class_ref=lms_class.id,
            user=user.id,
            role="member",
            is_active=True
        )
    except IntegrityError:
        return jsonify({"error": "Failed to join class"}), 500

    return jsonify({
        "message": "Successfully joined the class",
        "data": {
            "membership_id": membership.id,
            "class_id": lms_class.id,
            "class_title": lms_class.title,
            "user_id": user.id,
            "role": membership.role,
            "joined_at": membership.joined_at.isoformat() if membership.joined_at else None
        }
    }), 201
