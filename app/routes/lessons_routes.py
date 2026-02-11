from flask import Blueprint

from app.controllers.lessons.create_lesson import create_lesson_handler
from app.controllers.lessons.read_lesson import read_lesson_handler
from app.controllers.lessons.update_lesson import update_lesson_handler
from app.controllers.lessons.delete_lesson import delete_lesson_handler


lessons_bp = Blueprint("lessons", __name__, url_prefix="/lessons")


@lessons_bp.post("")
def create_lesson():
    """
    Create lesson
    ---
    tags:
      - Lessons
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - class_id
            - title
            - author_id
          properties:
            class_id:
              type: integer
            title:
              type: string
            author_id:
              type: integer
            summary:
              type: string
            content:
              type: string
            content_json:
              type: object
            is_published:
              type: boolean
    responses:
      201:
        description: Created
      404:
        description: Class or author not found
    """
    return create_lesson_handler()


@lessons_bp.get("")
def list_lessons():
    """
    List lessons
    ---
    tags:
      - Lessons
    parameters:
      - in: query
        name: page
        type: integer
      - in: query
        name: per_page
        type: integer
    responses:
      200:
        description: OK
    """
    return read_lesson_handler()


@lessons_bp.get("/<int:lesson_id>")
def get_lesson(lesson_id: int):
    """
    Get lesson by id
    ---
    tags:
      - Lessons
    parameters:
      - in: path
        name: lesson_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_lesson_handler(lesson_id=lesson_id)


@lessons_bp.put("/<int:lesson_id>")
@lessons_bp.patch("/<int:lesson_id>")
def update_lesson(lesson_id: int):
    """
    Update lesson
    ---
    tags:
      - Lessons
    consumes:
      - application/json
    parameters:
      - in: path
        name: lesson_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            title:
              type: string
            summary:
              type: string
            content:
              type: string
            content_json:
              type: object
            is_published:
              type: boolean
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_lesson_handler(lesson_id)


@lessons_bp.delete("/<int:lesson_id>")
def delete_lesson(lesson_id: int):
    """
    Delete lesson
    ---
    tags:
      - Lessons
    parameters:
      - in: path
        name: lesson_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_lesson_handler(lesson_id)
