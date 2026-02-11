from flask import Blueprint

from app.controllers.submissions.create_submission import create_submission_handler
from app.controllers.submissions.read_submission import read_submission_handler
from app.controllers.submissions.update_submission import update_submission_handler
from app.controllers.submissions.delete_submission import delete_submission_handler


submissions_bp = Blueprint("submissions", __name__, url_prefix="/submissions")


@submissions_bp.post("")
def create_submission():
    """
    Create submission
    ---
    tags:
      - Submissions
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - assignment_id
            - user_id
          properties:
            assignment_id:
              type: integer
            user_id:
              type: integer
            submitted_at:
              type: string
              format: date-time
            text_answer:
              type: string
            status:
              type: string
              enum: [pending, submitted, graded]
    responses:
      201:
        description: Created
      404:
        description: Assignment or user not found
      409:
        description: Submission already exists for assignment+user
    """
    return create_submission_handler()


@submissions_bp.get("")
def list_submissions():
    """
    List submissions
    ---
    tags:
      - Submissions
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
    return read_submission_handler()


@submissions_bp.get("/<int:submission_id>")
def get_submission(submission_id: int):
    """
    Get submission by id
    ---
    tags:
      - Submissions
    parameters:
      - in: path
        name: submission_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_submission_handler(submission_id=submission_id)


@submissions_bp.put("/<int:submission_id>")
@submissions_bp.patch("/<int:submission_id>")
def update_submission(submission_id: int):
    """
    Update submission
    ---
    tags:
      - Submissions
    consumes:
      - application/json
    parameters:
      - in: path
        name: submission_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            submitted_at:
              type: string
              format: date-time
            text_answer:
              type: string
            status:
              type: string
              enum: [pending, submitted, graded]
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_submission_handler(submission_id)


@submissions_bp.delete("/<int:submission_id>")
def delete_submission(submission_id: int):
    """
    Delete submission
    ---
    tags:
      - Submissions
    parameters:
      - in: path
        name: submission_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_submission_handler(submission_id)
