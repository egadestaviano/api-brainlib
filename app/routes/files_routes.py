from flask import Blueprint

from app.controllers.files.create_file import create_file_handler
from app.controllers.files.read_file import read_file_handler
from app.controllers.files.update_file import update_file_handler
from app.controllers.files.delete_file import delete_file_handler


files_bp = Blueprint("files", __name__, url_prefix="/files")


@files_bp.post("")
def create_file():
    """
    Create file record
    ---
    tags:
      - Files
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - owner_id
            - filename
          properties:
            owner_id:
              type: integer
            filename:
              type: string
            mime_type:
              type: string
            url:
              type: string
            path:
              type: string
            size_bytes:
              type: integer
            purpose:
              type: string
            storage_backend:
              type: string
            is_public:
              type: boolean
            reference_count:
              type: integer
            metadata:
              type: object
    responses:
      201:
        description: Created
      404:
        description: Owner not found
    """
    return create_file_handler()


@files_bp.get("")
def list_files():
    """
    List files
    ---
    tags:
      - Files
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
    return read_file_handler()


@files_bp.get("/<int:file_id>")
def get_file(file_id: int):
    """
    Get file by id
    ---
    tags:
      - Files
    parameters:
      - in: path
        name: file_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_file_handler(file_id=file_id)


@files_bp.put("/<int:file_id>")
@files_bp.patch("/<int:file_id>")
def update_file(file_id: int):
    """
    Update file record
    ---
    tags:
      - Files
    consumes:
      - application/json
    parameters:
      - in: path
        name: file_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            filename:
              type: string
            mime_type:
              type: string
            url:
              type: string
            path:
              type: string
            size_bytes:
              type: integer
            purpose:
              type: string
            storage_backend:
              type: string
            is_public:
              type: boolean
            reference_count:
              type: integer
            metadata:
              type: object
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_file_handler(file_id)


@files_bp.delete("/<int:file_id>")
def delete_file(file_id: int):
    """
    Delete file record
    ---
    tags:
      - Files
    parameters:
      - in: path
        name: file_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_file_handler(file_id)
