from flask import jsonify
from app.models.lms_class import LmsClass
from app.models.user import User, Role, UserRole
from app.models.class_membership import ClassMembership
from app.models.lesson import Lesson
from app.models.user_profile import UserProfile
from app.schemas.lms_class import ClassListSchema
from app.utils.auth import get_user_from_token
from peewee import fn, JOIN, prefetch

list_schema = ClassListSchema(many=True)

def read_my_class_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

    # Check if user is admin
    user_roles = [ur.role.name.lower() for ur in user.roles]
    is_admin = 'admin' in user_roles

    if is_admin:
        classes_query = LmsClass.select().order_by(LmsClass.id.desc())
    else:
        creator_query = LmsClass.select().where(LmsClass.creator == user)
        member_query = (
            LmsClass
            .select(LmsClass)
            .join(ClassMembership, on=(ClassMembership.class_ref == LmsClass.id))
            .where(
                (ClassMembership.user == user) &
                (ClassMembership.is_active == True)
            )
        )
        class_ids = set([c.id for c in creator_query] + [c.id for c in member_query])
        classes_query = LmsClass.select().where(LmsClass.id.in_(class_ids)).order_by(LmsClass.id.desc())

    # Prefetch creator and their profile
    classes = prefetch(
        classes_query,
        User.select().join(UserProfile, JOIN.LEFT_OUTER),
        UserProfile.select()
    )

    classes_with_data = []
    for cls in classes:
        # member_count
        member_count = (
            ClassMembership
            .select(fn.COUNT(ClassMembership.id))
            .where(
                (ClassMembership.class_ref == cls.id) &
                (ClassMembership.is_active == True)
            )
            .scalar() or 0
        )
        setattr(cls, "member_count", member_count)

        # lesson_count
        lesson_count = (
            Lesson
            .select(fn.COUNT(Lesson.id))
            .where(Lesson.class_ref == cls.id)
            .scalar() or 0
        )
        setattr(cls, "lesson_count", lesson_count)

        classes_with_data.append(cls)

    return jsonify({
        "data": list_schema.dump(classes_with_data),
    })
