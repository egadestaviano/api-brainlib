from flask import Blueprint

from app.controllers.presigned_uploads.create_presigned_upload import create_presigned_upload_handler
from app.controllers.presigned_uploads.read_presigned_upload import read_presigned_upload_handler
from app.controllers.presigned_uploads.update_presigned_upload import update_presigned_upload_handler
from app.controllers.presigned_uploads.delete_presigned_upload import delete_presigned_upload_handler


presigned_upload_bp = Blueprint("presigned_uploads", __name__, url_prefix="/presigned-uploads")


@presigned_upload_bp.post("")
def create_presigned_upload():
    """
    Create presigned upload
    ---
    tags:
      - PresignedUploads
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - key
            - expires_at
          properties:
            user_id:
              type: integer
            key:
              type: string
            mime_type:
              type: string
            filename:
              type: string
            expires_at:
              type: string
              format: date-time
            completed:
              type: boolean
    responses:
      201:
        description: Created
      404:
        description: User not found
      409:
        description: Key already exists
    """
    return create_presigned_upload_handler()


@presigned_upload_bp.get("")
def list_presigned_uploads():
    """
    List presigned uploads
    ---
    tags:
      - PresignedUploads
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
    return read_presigned_upload_handler()


@presigned_upload_bp.get("/<int:pu_id>")
def get_presigned_upload(pu_id: int):
    """
    Get presigned upload by id
    ---
    tags:
      - PresignedUploads
    parameters:
      - in: path
        name: pu_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_presigned_upload_handler(pu_id=pu_id)


@presigned_upload_bp.put("/<int:pu_id>")
@presigned_upload_bp.patch("/<int:pu_id>")
def update_presigned_upload(pu_id: int):
    """
    Update presigned upload
    ---
    tags:
      - PresignedUploads
    consumes:
      - application/json
    parameters:
      - in: path
        name: pu_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            key:
              type: string
            mime_type:
              type: string
            filename:
              type: string
            expires_at:
              type: string
              format: date-time
            completed:
              type: boolean
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_presigned_upload_handler(pu_id)


@presigned_upload_bp.delete("/<int:pu_id>")
def delete_presigned_upload(pu_id: int):
    """
    Delete presigned upload
    ---
    tags:
      - PresignedUploads
    parameters:
      - in: path
        name: pu_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_presigned_upload_handler(pu_id)
