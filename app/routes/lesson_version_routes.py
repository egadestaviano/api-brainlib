from flask import Blueprint

from app.controllers.lesson_versions.create_lesson_version import create_lesson_version_handler
from app.controllers.lesson_versions.read_lesson_version import read_lesson_version_handler
from app.controllers.lesson_versions.update_lesson_version import update_lesson_version_handler
from app.controllers.lesson_versions.delete_lesson_version import delete_lesson_version_handler


lesson_version_bp = Blueprint("lesson_versions", __name__, url_prefix="/lesson-versions")


@lesson_version_bp.post("")
def create_lesson_version():
    """
    Create lesson version
    ---
    tags:
      - LessonVersions
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - lesson_id
            - version_number
            - author_id
          properties:
            lesson_id:
              type: integer
            version_number:
              type: integer
            author_id:
              type: integer
            content_json:
              type: object
    responses:
      201:
        description: Created
      404:
        description: Lesson or author not found
      409:
        description: Conflict (version exists)
    """
    return create_lesson_version_handler()


@lesson_version_bp.get("")
def list_lesson_versions():
    """
    List lesson versions
    ---
    tags:
      - LessonVersions
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
    return read_lesson_version_handler()


@lesson_version_bp.get("/<int:version_id>")
def get_lesson_version(version_id: int):
    """
    Get lesson version by id
    ---
    tags:
      - LessonVersions
    parameters:
      - in: path
        name: version_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return read_lesson_version_handler(version_id=version_id)


@lesson_version_bp.put("/<int:version_id>")
@lesson_version_bp.patch("/<int:version_id>")
def update_lesson_version(version_id: int):
    """
    Update lesson version
    ---
    tags:
      - LessonVersions
    consumes:
      - application/json
    parameters:
      - in: path
        name: version_id
        type: integer
        required: true
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            version_number:
              type: integer
            content_json:
              type: object
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return update_lesson_version_handler(version_id)


@lesson_version_bp.delete("/<int:version_id>")
def delete_lesson_version(version_id: int):
    """
    Delete lesson version
    ---
    tags:
      - LessonVersions
    parameters:
      - in: path
        name: version_id
        type: integer
        required: true
    responses:
      200:
        description: OK
      404:
        description: Not Found
    """
    return delete_lesson_version_handler(version_id)
