from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    BooleanField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.lms_class import LmsClass
from app.models.lesson import Lesson
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class Assignment(BaseModel):
    id = AutoField()
    class_ref = ForeignKeyField(LmsClass, backref='assignments', on_delete='CASCADE', on_update='CASCADE', column_name='class_id')
    lesson = ForeignKeyField(Lesson, backref='assignments', null=True, on_delete='SET NULL', on_update='CASCADE')
    title = CharField(max_length=255)
    description = TextField(null=True)
    instructions = TextField(null=True)
    creator = ForeignKeyField(User, backref='assignments', on_delete='CASCADE', on_update='CASCADE', column_name='creator_id')
    due_at = DateTimeField(null=True)
    allow_file_upload = BooleanField(default=False)
    max_score = IntegerField(default=100)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "assignments"
