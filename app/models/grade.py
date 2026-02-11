from peewee import (
    Model,
    AutoField,
    IntegerField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.submission import Submission
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class Grade(BaseModel):
    id = AutoField()
    submission = ForeignKeyField(Submission, backref='grades', on_delete='CASCADE', on_update='CASCADE', column_name='submission_id')
    grader = ForeignKeyField(User, backref='grades_given', on_delete='CASCADE', on_update='CASCADE', column_name='grader_id')
    score = IntegerField()
    feedback = TextField(null=True)
    graded_at = DateTimeField()

    class Meta:
        table_name = "grades"
