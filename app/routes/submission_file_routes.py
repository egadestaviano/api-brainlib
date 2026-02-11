from flask import Blueprint

from app.controllers.submission_files.create_submission_file import create_submission_file_handler
from app.controllers.submission_files.read_submission_file import read_submission_file_handler
from app.controllers.submission_files.update_submission_file import update_submission_file_handler
from app.controllers.submission_files.delete_submission_file import delete_submission_file_handler


submission_file_bp = Blueprint("submission_files", __name__, url_prefix="/submission-files")


@submission_file_bp.post("")
def create_submission_file():
    """
    Create submission-file mapping
    ---
    tags:
      - SubmissionFiles
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
            - file_id
          properties:
            submission_id:
              type: integer
            file_id:
              type: integer
    responses:
      201:
        description: Created
      404:
        description: Submission not found
      409:
        description: Duplicate mapping
    """
    return create_submission_file_handler()


@submission_file_bp.get("")
def list_submission_files():
    """
    List submission-files
    ---
    tags:
      - SubmissionFiles
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
    return read_submission_file_handler()


@submission_file_bp.get("/<int:pivot_id>")
def get_submission_file(pivot_id: int):
    """
    Get submission-file by id
    ---
    tags:
      - SubmissionFiles
    parameters:
      - in: path
        name: pivot_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_submission_file_handler(pivot_id=pivot_id)


@submission_file_bp.put("/<int:pivot_id>")
@submission_file_bp.patch("/<int:pivot_id>")
def update_submission_file(pivot_id: int):
    """
    Update submission-file mapping
    ---
    tags:
      - SubmissionFiles
    consumes:
      - application/json
    parameters:
      - in: path
        name: pivot_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            submission_id:
              type: integer
            file_id:
              type: integer
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_submission_file_handler(pivot_id)


@submission_file_bp.delete("/<int:pivot_id>")
def delete_submission_file(pivot_id: int):
    """
    Delete submission-file mapping
    ---
    tags:
      - SubmissionFiles
    parameters:
      - in: path
        name: pivot_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_submission_file_handler(pivot_id)
