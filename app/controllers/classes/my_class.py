from flask import jsonify
from app.models.lms_class import LmsClass
from app.models.class_membership import ClassMembership
from app.models.user_profile import UserProfile
from app.schemas.lms_class import ClassListSchema
from app.utils.auth import get_user_from_token
from peewee import fn

list_schema = ClassListSchema(many=True)

def read_my_class_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

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

    classes = LmsClass.select().where(LmsClass.id.in_(class_ids))

    classes_with_creator = []
    for cls in classes:
        creator = cls.creator
        try:
            profile_obj = UserProfile.get(UserProfile.user == creator.id)
            setattr(creator, "profile", [profile_obj])
        except UserProfile.DoesNotExist:
            setattr(creator, "profile", [])

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

        classes_with_creator.append(cls)

    return jsonify({
        "data": list_schema.dump(classes_with_creator),
    })
