from flask import Blueprint

from app.controllers.user_profiles.create_user_profile import create_user_profile_handler
from app.controllers.user_profiles.read_user_profile import read_user_profile_handler
from app.controllers.user_profiles.update_user_profile import update_user_profile_handler
from app.controllers.user_profiles.delete_user_profile import delete_user_profile_handler


user_profile_bp = Blueprint("user_profiles", __name__, url_prefix="/user-profiles")


@user_profile_bp.post("")
def create_user_profile():
    """
    Create user profile
    ---
    tags:
      - UserProfiles
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
          properties:
            user_id:
              type: integer
            display_name:
              type: string
            avatar_file_id:
              type: integer
            bio:
              type: string
            extra:
              type: object
    responses:
      201:
        description: Created
      404:
        description: User not found
      409:
        description: Conflict (already exists)
    """
    return create_user_profile_handler()


@user_profile_bp.get("")
def list_user_profiles():
    """
    List user profiles
    ---
    tags:
      - UserProfiles
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
    return read_user_profile_handler()


@user_profile_bp.get("/<int:profile_id>")
def get_user_profile(profile_id: int):
    """
    Get user profile by id
    ---
    tags:
      - UserProfiles
    parameters:
      - in: path
        name: profile_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_user_profile_handler(profile_id=profile_id)


@user_profile_bp.put("/<int:profile_id>")
@user_profile_bp.patch("/<int:profile_id>")
def update_user_profile(profile_id: int):
    """
    Update user profile
    ---
    tags:
      - UserProfiles
    consumes:
      - application/json
    parameters:
      - in: path
        name: profile_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            display_name:
              type: string
            avatar_file_id:
              type: integer
            bio:
              type: string
            extra:
              type: object
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_user_profile_handler(profile_id)


@user_profile_bp.delete("/<int:profile_id>")
def delete_user_profile(profile_id: int):
    """
    Delete user profile
    ---
    tags:
      - UserProfiles
    parameters:
      - in: path
        name: profile_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_user_profile_handler(profile_id)
