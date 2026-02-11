from flask import Blueprint

from app.controllers.class_memberships.create_class_membership import create_class_membership_handler
from app.controllers.class_memberships.read_class_membership import read_class_membership_handler
from app.controllers.class_memberships.update_class_membership import update_class_membership_handler
from app.controllers.class_memberships.delete_class_membership import delete_class_membership_handler


class_membership_bp = Blueprint("class_memberships", __name__, url_prefix="/class-memberships")


@class_membership_bp.post("")
def create_class_membership():
    """
    Create class membership
    ---
    tags:
      - ClassMemberships
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
            - user_id
          properties:
            class_id:
              type: integer
            user_id:
              type: integer
            role:
              type: string
            is_active:
              type: boolean
    responses:
      201:
        description: Created
      404:
        description: Class or user not found
      409:
        description: Conflict (already exists)
    """
    return create_class_membership_handler()


@class_membership_bp.get("")
def list_class_memberships():
    """
    List class memberships
    ---
    tags:
      - ClassMemberships
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
    return read_class_membership_handler()


@class_membership_bp.get("/<int:membership_id>")
def get_class_membership(membership_id: int):
    """
    Get class membership by id
    ---
    tags:
      - ClassMemberships
    parameters:
      - in: path
        name: membership_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_class_membership_handler(membership_id=membership_id)


@class_membership_bp.put("/<int:membership_id>")
@class_membership_bp.patch("/<int:membership_id>")
def update_class_membership(membership_id: int):
    """
    Update class membership
    ---
    tags:
      - ClassMemberships
    consumes:
      - application/json
    parameters:
      - in: path
        name: membership_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            role:
              type: string
            is_active:
              type: boolean
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_class_membership_handler(membership_id)


@class_membership_bp.delete("/<int:membership_id>")
def delete_class_membership(membership_id: int):
    """
    Delete class membership
    ---
    tags:
      - ClassMemberships
    parameters:
      - in: path
        name: membership_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_class_membership_handler(membership_id)
