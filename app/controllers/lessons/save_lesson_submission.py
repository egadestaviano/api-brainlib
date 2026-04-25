from flask import request, jsonify
from peewee import IntegrityError
from datetime import datetime
import json

from app.models.lesson_submission import LessonSubmission
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.lesson_submission import LessonSubmissionSchema

schema = LessonSubmissionSchema()

def save_lesson_submission_handler():
    payload = request.get_json(silent=True) or {}
    
    lesson_id = payload.get("lesson_id")
    user_id = payload.get("user_id")
    
    if not lesson_id or not user_id:
        return jsonify({"error": "lesson_id and user_id are required"}), 400
        
    lesson = Lesson.get_or_none(Lesson.id == lesson_id)
    if not lesson:
        return jsonify({"error": "lesson not found"}), 404
        
    user = User.get_or_none(User.id == user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
        
    answers_json = payload.get("answers_json")
    submitted_at = payload.get("submitted_at")
    
    # Parse submitted_at if present
    if submitted_at:
        try:
            submitted_at = datetime.fromisoformat(submitted_at.replace("Z", "+00:00"))
        except:
            submitted_at = datetime.now()
    else:
        submitted_at = None

    try:
        # Check if already exists
        row = LessonSubmission.get_or_none((LessonSubmission.lesson == lesson_id) & (LessonSubmission.user == user_id))
        
        if row:
            # If already submitted and user tries to save again, we should probably check if it's allowed
            # The requirement says "tidak bisa dikerjakan kembali"
            if row.submitted_at and submitted_at:
                 return jsonify({"error": "Lesson already submitted and locked"}), 403
            
            row.answers_json = answers_json or row.answers_json
            if submitted_at:
                row.submitted_at = submitted_at
            row.updated_at = datetime.now()
            row.save()
        else:
            row = LessonSubmission.create(
                lesson=lesson_id,
                user=user_id,
                answers_json=answers_json,
                submitted_at=submitted_at,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
        return jsonify(schema.dump(row)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
