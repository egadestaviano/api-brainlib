from peewee import (
    Model,
    AutoField,
    IntegerField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.lesson import Lesson
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class LessonVersion(BaseModel):
    id = AutoField()
    lesson = ForeignKeyField(Lesson, backref='versions', on_delete='CASCADE', on_update='CASCADE', column_name='lesson_id')
    version_number = IntegerField()
    content_json = TextField(null=True)
    author = ForeignKeyField(User, backref='lesson_versions', on_delete='CASCADE', on_update='CASCADE', column_name='author_id')
    created_at = DateTimeField()

    class Meta:
        table_name = "lessons_version"
        indexes = (
            (('lesson', 'version_number'), True),
        )
