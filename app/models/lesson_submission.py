from peewee import (
    Model,
    AutoField,
    TextField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.lesson import Lesson
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class LessonSubmission(BaseModel):
    id = AutoField()
    lesson = ForeignKeyField(Lesson, backref='submissions', on_delete='CASCADE', on_update='CASCADE', column_name='lesson_id')
    user = ForeignKeyField(User, backref='lesson_submissions', on_delete='CASCADE', on_update='CASCADE', column_name='user_id')
    results_json = TextField()
    score_correct = IntegerField(default=0)
    score_wrong = IntegerField(default=0)
    submitted_at = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "lesson_submissions"
        indexes = (
            (('lesson', 'user'), True),
        )
