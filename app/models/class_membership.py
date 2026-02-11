from peewee import (
    Model,
    AutoField,
    CharField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    CompositeKey,
)
from app.db import database
from app.models.lms_class import LmsClass
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class ClassMembership(BaseModel):
    id = AutoField()
    class_ref = ForeignKeyField(LmsClass, backref='memberships', on_delete='CASCADE', on_update='CASCADE', column_name='class_id')
    user = ForeignKeyField(User, backref='class_memberships', on_delete='CASCADE', on_update='CASCADE')
    role = CharField(max_length=32, default='member')
    joined_at = DateTimeField()
    is_active = BooleanField(default=True)

    class Meta:
        table_name = "class_memberships"
        indexes = (
            (('class_ref', 'user'), True),
        )
