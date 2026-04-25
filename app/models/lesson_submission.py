from peewee import (
    Model,
    AutoField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.lesson import Lesson
from app.models.user import User
from datetime import datetime

class BaseModel(Model):
    class Meta:
        database = database

class LessonSubmission(BaseModel):
    id = AutoField()
    lesson = ForeignKeyField(Lesson, backref='lesson_submissions', on_delete='CASCADE', on_update='CASCADE', column_name='lesson_id')
    user = ForeignKeyField(User, backref='lesson_submissions', on_delete='CASCADE', on_update='CASCADE', column_name='user_id')
    answers_json = TextField(null=True)
    submitted_at = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "lesson_submissions"
        indexes = (
            (('lesson', 'user'), True),
        )
