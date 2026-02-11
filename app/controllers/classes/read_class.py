from flask import jsonify
from peewee import prefetch, JOIN
from app.models.lms_class import LmsClass
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.lesson import Lesson
from app.models.class_membership import ClassMembership
from app.schemas.lms_class import ClassListSchema, ClassDetailSchema

list_schema = ClassListSchema(many=True)
detail_schema = ClassDetailSchema()

def read_class_handler(class_id=None):
    base_query = LmsClass.select().order_by(LmsClass.id)

    related_query = prefetch(
        base_query,
        Lesson.select().join(User),
        ClassMembership.select().join(User),
        User.select().join(UserProfile, JOIN.LEFT_OUTER),
        UserProfile.select()
    )

    if class_id is not None:
        result = next((r for r in related_query if r.id == class_id), None)
        if not result:
            return jsonify({"error": "class not found"}), 404

        data = detail_schema.dump(result)
        return jsonify(data)

    # jika ambil list semua class
    data = list_schema.dump(related_query)
    return jsonify({"data": data})
