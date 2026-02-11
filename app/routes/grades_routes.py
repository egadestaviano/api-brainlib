from flask import Blueprint

from app.controllers.grades.create_grade import create_grade_handler
from app.controllers.grades.read_grade import read_grade_handler
from app.controllers.grades.update_grade import update_grade_handler
from app.controllers.grades.delete_grade import delete_grade_handler


grades_bp = Blueprint("grades", __name__, url_prefix="/grades")


@grades_bp.post("")
def create_grade():
    """
    Create grade
    ---
    tags:
      - Grades
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - submission_id
            - grader_id
            - score
          properties:
            submission_id:
              type: integer
            grader_id:
              type: integer
            score:
              type: integer
            feedback:
              type: string
    responses:
      201:
        description: Created
      404:
        description: Submission or grader not found
    """
    return create_grade_handler()


@grades_bp.get("")
def list_grades():
    """
    List grades
    ---
    tags:
      - Grades
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
    return read_grade_handler()


@grades_bp.get("/<int:grade_id>")
def get_grade(grade_id: int):
    """
    Get grade by id
    ---
    tags:
      - Grades
    parameters:
      - in: path
        name: grade_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_grade_handler(grade_id=grade_id)


@grades_bp.put("/<int:grade_id>")
@grades_bp.patch("/<int:grade_id>")
def update_grade(grade_id: int):
    """
    Update grade
    ---
    tags:
      - Grades
    consumes:
      - application/json
    parameters:
      - in: path
        name: grade_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            score:
              type: integer
            feedback:
              type: string
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_grade_handler(grade_id)


@grades_bp.delete("/<int:grade_id>")
def delete_grade(grade_id: int):
    """
    Delete grade
    ---
    tags:
      - Grades
    parameters:
      - in: path
        name: grade_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_grade_handler(grade_id)
