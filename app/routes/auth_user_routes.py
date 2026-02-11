from flask import Blueprint

from app.controllers.auth.register_auth import register_user_handler
from app.controllers.auth.login_auth import login_user_handler
from app.controllers.auth.me_auth import me_user_handler

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register_user():
    """
    Register new user
    ---
    tags:
      - Auth
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
      400:
        description: Validation error
      409:
        description: Conflict (email exists)
    """
    return register_user_handler()


@auth_bp.post("/login")
def login_user():
    """
    User login
    ---
    tags:
      - Auth
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
    responses:
      200:
        description: OK (returns token + user)
      401:
        description: Unauthorized
    """
    return login_user_handler()


@auth_bp.get("/me")
def me_user():
    """
    Get current authenticated user
    ---
    tags:
      - Auth
    security:
      - bearerAuth: []
    responses:
      200:
        description: OK
      401:
        description: Unauthorized
    """
    return me_user_handler()
