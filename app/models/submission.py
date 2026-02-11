from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.assignment import Assignment
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class Submission(BaseModel):
    id = AutoField()
    assignment = ForeignKeyField(Assignment, backref='submissions', on_delete='CASCADE', on_update='CASCADE', column_name='assignment_id')
    user = ForeignKeyField(User, backref='submissions', on_delete='CASCADE', on_update='CASCADE')
    submitted_at = DateTimeField(null=True)
    text_answer = TextField(null=True)
    status = CharField(max_length=32, default='pending')
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "submissions"
        indexes = (
            (('assignment', 'user'), True),
        )
