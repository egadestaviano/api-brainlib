from flask import request, jsonify
from app.models.lesson_submission import LessonSubmission
from app.schemas.lesson_submission import LessonSubmissionSchema

schema = LessonSubmissionSchema()

def get_lesson_submission_handler(lesson_id, user_id):
    row = LessonSubmission.get_or_none((LessonSubmission.lesson == lesson_id) & (LessonSubmission.user == user_id))
    if not row:
        return jsonify({"message": "No submission found"}), 404
        
    return jsonify(schema.dump(row)), 200
