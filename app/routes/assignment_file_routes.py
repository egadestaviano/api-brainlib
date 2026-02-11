from flask import Blueprint

from app.controllers.assignment_files.create_assignment_file import create_assignment_file_handler
from app.controllers.assignment_files.read_assignment_file import read_assignment_file_handler
from app.controllers.assignment_files.update_assignment_file import update_assignment_file_handler
from app.controllers.assignment_files.delete_assignment_file import delete_assignment_file_handler


assignment_file_bp = Blueprint("assignment_files", __name__, url_prefix="/assignment-files")


@assignment_file_bp.post("")
def create_assignment_file():
    """
    Create assignment-file mapping
    ---
    tags:
      - AssignmentFiles
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
            - file_id
          properties:
            assignment_id:
              type: integer
            file_id:
              type: integer
    responses:
      201:
        description: Created
      404:
        description: Assignment not found
      409:
        description: Duplicate mapping
    """
    return create_assignment_file_handler()


@assignment_file_bp.get("")
def list_assignment_files():
    """
    List assignment-files
    ---
    tags:
      - AssignmentFiles
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
    return read_assignment_file_handler()


@assignment_file_bp.get("/<int:pivot_id>")
def get_assignment_file(pivot_id: int):
    """
    Get assignment-file by id
    ---
    tags:
      - AssignmentFiles
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
    return read_assignment_file_handler(pivot_id=pivot_id)


@assignment_file_bp.put("/<int:pivot_id>")
@assignment_file_bp.patch("/<int:pivot_id>")
def update_assignment_file(pivot_id: int):
    """
    Update assignment-file mapping
    ---
    tags:
      - AssignmentFiles
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
            assignment_id:
              type: integer
            file_id:
              type: integer
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_assignment_file_handler(pivot_id)


@assignment_file_bp.delete("/<int:pivot_id>")
def delete_assignment_file(pivot_id: int):
    """
    Delete assignment-file mapping
    ---
    tags:
      - AssignmentFiles
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
    return delete_assignment_file_handler(pivot_id)
