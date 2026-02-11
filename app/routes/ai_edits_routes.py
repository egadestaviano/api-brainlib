from flask import Blueprint

from app.controllers.ai_edits.create_ai_edit import create_ai_edit_handler
from app.controllers.ai_edits.read_ai_edit import read_ai_edit_handler
from app.controllers.ai_edits.update_ai_edit import update_ai_edit_handler
from app.controllers.ai_edits.delete_ai_edit import delete_ai_edit_handler


ai_edits_bp = Blueprint("ai_edits", __name__, url_prefix="/ai-edits")


@ai_edits_bp.post("")
def create_ai_edit():
    """
    Create AI edit record
    ---
    tags:
      - AIedits
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - target_table
            - target_id
            - editor_service
          properties:
            target_table:
              type: string
            target_id:
              type: integer
            original_content:
              type: string
            edited_content:
              type: string
            editor_service:
              type: string
            user_id:
              type: integer
              nullable: true
    responses:
      201:
        description: Created
      404:
        description: User not found
    """
    return create_ai_edit_handler()


@ai_edits_bp.get("")
def list_ai_edits():
    """
    List AI edits
    ---
    tags:
      - AIedits
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
    return read_ai_edit_handler()


@ai_edits_bp.get("/<int:ai_edit_id>")
def get_ai_edit(ai_edit_id: int):
    """
    Get AI edit by id
    ---
    tags:
      - AIedits
    parameters:
      - in: path
        name: ai_edit_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_ai_edit_handler(ai_edit_id=ai_edit_id)


@ai_edits_bp.put("/<int:ai_edit_id>")
@ai_edits_bp.patch("/<int:ai_edit_id>")
def update_ai_edit(ai_edit_id: int):
    """
    Update AI edit
    ---
    tags:
      - AIedits
    consumes:
      - application/json
    parameters:
      - in: path
        name: ai_edit_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            target_table:
              type: string
            target_id:
              type: integer
            original_content:
              type: string
            edited_content:
              type: string
            editor_service:
              type: string
            user_id:
              type: integer
              nullable: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_ai_edit_handler(ai_edit_id)


@ai_edits_bp.delete("/<int:ai_edit_id>")
def delete_ai_edit(ai_edit_id: int):
    """
    Delete AI edit
    ---
    tags:
      - AIedits
    parameters:
      - in: path
        name: ai_edit_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_ai_edit_handler(ai_edit_id)
