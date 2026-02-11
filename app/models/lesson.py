from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.lms_class import LmsClass
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class Lesson(BaseModel):
    id = AutoField()
    class_ref = ForeignKeyField(LmsClass, backref='lessons', on_delete='CASCADE', on_update='CASCADE', column_name='class_id')
    title = CharField(max_length=255)
    summary = TextField(null=True)
    content = TextField(null=True)
    content_json = TextField(null=True)
    author = ForeignKeyField(User, backref='lessons', on_delete='CASCADE', on_update='CASCADE', column_name='author_id')
    is_published = BooleanField(default=False)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "lessons"
