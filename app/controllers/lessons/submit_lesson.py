import json
import datetime
from flask import request, jsonify
from app.models.lesson_submission import LessonSubmission
from app.models.lesson import Lesson
from app.utils.auth import get_user_from_token

def submit_lesson_handler(lesson_id):
    user, _, error = get_user_from_token()
    if error:
        return error
    
    lesson = Lesson.get_or_none(Lesson.id == lesson_id)
    if not lesson:
        return jsonify({"error": "lesson not found"}), 404
    
    payload = request.get_json(silent=True) or {}
    results = payload.get("results", {})
    score_correct = payload.get("score_correct", 0)
    score_wrong = payload.get("score_wrong", 0)
    
    print(f"DEBUG: submit_lesson_handler - user_id: {user.id}, lesson_id: {lesson_id}")
    print(f"DEBUG: payload: {json.dumps(payload)}")
    
    now = datetime.datetime.utcnow()
    
    try:
        submission, created = LessonSubmission.get_or_create(
            lesson=lesson,
            user=user,
            defaults={
                "results_json": json.dumps(results),
                "score_correct": score_correct,
                "score_wrong": score_wrong,
                "submitted_at": now,
                "created_at": now,
                "updated_at": now
            }
        )
        
        if not created:
            print(f"DEBUG: Submission already exists for user {user.id} and lesson {lesson_id}")
            return jsonify({"error": "lesson already submitted"}), 409
        
        print(f"DEBUG: Submission created successfully for user {user.id}, id: {submission.id}")
        return jsonify({"message": "submitted successfully", "id": submission.id}), 201
        
    except Exception as e:
        print(f"ERROR: Failed to save submission: {str(e)}")
        return jsonify({"error": f"Failed to save submission: {str(e)}"}), 500

def get_lesson_submission_handler(lesson_id):
    user, _, error = get_user_from_token()
    if error:
        return error
    
    submission = LessonSubmission.get_or_none(
        (LessonSubmission.lesson == lesson_id) & (LessonSubmission.user == user.id)
    )
    
    if not submission:
        return jsonify({"data": None}), 200
    
    return jsonify({
        "data": {
            "id": submission.id,
            "results": json.loads(submission.results_json),
            "score_correct": submission.score_correct,
            "score_wrong": submission.score_wrong,
            "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None
        }
    }), 200

def list_lesson_submissions_handler(lesson_id):
    user, _, error = get_user_from_token()
    if error:
        return error
    
    from app.models.user import User
    from app.models.user_profile import UserProfile
    from peewee import JOIN

    # Join User and UserProfile to get names efficiently
    submissions = (LessonSubmission
                  .select(LessonSubmission, User, UserProfile)
                  .join(User, on=(LessonSubmission.user == User.id))
                  .join(UserProfile, JOIN.LEFT_OUTER, on=(User.id == UserProfile.user))
                  .where(LessonSubmission.lesson == lesson_id))
    
    data = []
    for s in submissions:
        # Robust name detection
        display_name = s.user.email
        try:
            # Peewee models with joins might have the related object attached
            if hasattr(s.user, 'user_profile'):
                profile = s.user.user_profile
                if profile and profile.display_name:
                    display_name = profile.display_name
            elif hasattr(s.user, 'profile'): # Check our other backref name
                profile = s.user.profile
                if profile and profile.display_name:
                    display_name = profile.display_name
        except:
            pass

        data.append({
            "id": s.id,
            "user_id": s.user.id,
            "user_name": display_name,
            "score_correct": s.score_correct,
            "score_wrong": s.score_wrong,
            "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None
        })
    
    return jsonify({"data": data}), 200

