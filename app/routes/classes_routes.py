from flask import Blueprint

from app.controllers.classes.create_class import create_class_handler
from app.controllers.classes.read_class import read_class_handler
from app.controllers.classes.update_class import update_class_handler
from app.controllers.classes.delete_class import delete_class_handler
from app.controllers.classes.my_class import read_my_class_handler
from app.controllers.classes.join_class import join_class_by_code_handler


classes_bp = Blueprint("classes", __name__, url_prefix="/classes")


@classes_bp.post("")
def create_class():
    """
    Create class
    ---
    tags:
      - Classes
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Created
      404:
        description: Creator not found
      409:
        description: Conflict (code exists)
    """
    return create_class_handler()


@classes_bp.get("")
def list_classes():
    """
    List classes
    ---
    tags:
      - Classes
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
    return read_class_handler()
  
@classes_bp.post("/join")
def join_class_by_code():
    """
    Join class by code
    ---
    tags:
      - Classes
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - code
          properties:
            code:
              type: string
              example: "ABCD1234"
    responses:
      201:
        description: Joined successfully
      400:
        description: Missing code
      404:
        description: Invalid class code
      409:
        description: Already a member
    """
    return join_class_by_code_handler()



@classes_bp.get("/<int:class_id>")
def get_class(class_id: int):
    """
    Get class by id
    ---
    tags:
      - Classes
    parameters:
      - in: path
        name: class_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_class_handler(class_id=class_id)
  
@classes_bp.get("/my")
def my_classes():
    """
    List classes for current user (creator or member)
    ---
    tags:
      - Classes
    responses:
      200:
        description: OK
    """
    return read_my_class_handler()


@classes_bp.put("/<int:class_id>")
@classes_bp.patch("/<int:class_id>")
def update_class(class_id: int):
    """
    Update class
    ---
    tags:
      - Classes
    consumes:
      - application/json
    parameters:
      - in: path
        name: class_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            title:
              type: string
            code:
              type: string
            description:
              type: string
            visibility:
              type: string
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_class_handler(class_id)


@classes_bp.delete("/<int:class_id>")
def delete_class(class_id: int):
    """
    Delete class
    ---
    tags:
      - Classes
    parameters:
      - in: path
        name: class_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_class_handler(class_id)
