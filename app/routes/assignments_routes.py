from flask import Blueprint

from app.controllers.assignments.create_assignment import create_assignment_handler
from app.controllers.assignments.read_assignment import read_assignment_handler
from app.controllers.assignments.update_assignment import update_assignment_handler
from app.controllers.assignments.delete_assignment import delete_assignment_handler


assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")


@assignments_bp.post("")
def create_assignment():
    """
    Create assignment
    ---
    tags:
      - Assignments
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
            - creator_id
          properties:
            class_id:
              type: integer
            lesson_id:
              type: integer
              nullable: true
            title:
              type: string
            description:
              type: string
            instructions:
              type: string
            creator_id:
              type: integer
            due_at:
              type: string
              format: date-time
            allow_file_upload:
              type: boolean
            max_score:
              type: integer
    responses:
      201:
        description: Created
      404:
        description: Class, lesson, or creator not found
    """
    return create_assignment_handler()


@assignments_bp.get("")
def list_assignments():
    """
    List assignments
    ---
    tags:
      - Assignments
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
    return read_assignment_handler()


@assignments_bp.get("/<int:assignment_id>")
def get_assignment(assignment_id: int):
    """
    Get assignment by id
    ---
    tags:
      - Assignments
    parameters:
      - in: path
        name: assignment_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_assignment_handler(assignment_id=assignment_id)


@assignments_bp.put("/<int:assignment_id>")
@assignments_bp.patch("/<int:assignment_id>")
def update_assignment(assignment_id: int):
    """
    Update assignment
    ---
    tags:
      - Assignments
    consumes:
      - application/json
    parameters:
      - in: path
        name: assignment_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            class_id:
              type: integer
            lesson_id:
              type: integer
              nullable: true
            title:
              type: string
            description:
              type: string
            instructions:
              type: string
            due_at:
              type: string
              format: date-time
            allow_file_upload:
              type: boolean
            max_score:
              type: integer
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_assignment_handler(assignment_id)


@assignments_bp.delete("/<int:assignment_id>")
def delete_assignment(assignment_id: int):
    """
    Delete assignment
    ---
    tags:
      - Assignments
    parameters:
      - in: path
        name: assignment_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_assignment_handler(assignment_id)
