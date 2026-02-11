from flask import Blueprint

from app.controllers.users.create_user import create_user_handler
from app.controllers.users.read_user import read_user_handler
from app.controllers.users.update_user import update_user_handler
from app.controllers.users.delete_user import delete_user_handler


user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.post("")
def create_user():
    """
    Create user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
            is_active:
              type: boolean
    responses:
      201:
        description: Created
      409:
        description: Conflict (email exists)
    """
    return create_user_handler()


@user_bp.get("")
def list_users():
    """
    List users
    ---
    tags:
      - Users
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
    return read_user_handler()


@user_bp.get("/<int:user_id>")
def get_user(user_id: int):
    """
    Get user by id
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_user_handler(user_id=user_id)


@user_bp.put("/<int:user_id>")
@user_bp.patch("/<int:user_id>")
def update_user(user_id: int):
    """
    Update user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_user_handler(user_id)


@user_bp.delete("/<int:user_id>")
def delete_user(user_id: int):
    """
    Delete user
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_user_handler(user_id)
