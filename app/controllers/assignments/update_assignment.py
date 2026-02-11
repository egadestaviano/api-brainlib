from flask import request, jsonify
from datetime import datetime

from app.models.assignment import Assignment
from app.models.lms_class import LmsClass
from app.models.lesson import Lesson
from app.schemas.assignment import AssignmentSchema

schema = AssignmentSchema()


def _parse_due_at(value):
    if value in (None, "", 0):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def update_assignment_handler(assignment_id):
    row = Assignment.get_or_none(Assignment.id == assignment_id)
    if not row:
        return jsonify({"error": "assignment not found"}), 404

    payload = request.get_json(silent=True) or {}

    if "class_id" in payload:
        cid = payload.get("class_id")
        if not LmsClass.get_or_none(LmsClass.id == cid):
            return jsonify({"error": "class not found"}), 404
        row.class_ref = cid

    if "lesson_id" in payload:
        lid = payload.get("lesson_id")
        if lid in (None, ""):
            row.lesson = None
        else:
            if not Lesson.get_or_none(Lesson.id == lid):
                return jsonify({"error": "lesson not found"}), 404
            row.lesson = lid

    if "title" in payload:
        row.title = payload.get("title")
    if "description" in payload:
        row.description = payload.get("description")
    if "instructions" in payload:
        row.instructions = payload.get("instructions")
    if "due_at" in payload:
        parsed = _parse_due_at(payload.get("due_at"))
        if payload.get("due_at") is not None and parsed is None:
            return jsonify({"error": "due_at must be ISO datetime"}), 400
        row.due_at = parsed
    if "allow_file_upload" in payload:
        row.allow_file_upload = bool(payload.get("allow_file_upload"))
    if "max_score" in payload:
        try:
            row.max_score = int(payload.get("max_score"))
        except Exception:
            return jsonify({"error": "max_score must be integer"}), 400

    row.save()
    return jsonify(schema.dump(row))
