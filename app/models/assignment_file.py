from peewee import (
    Model,
    AutoField,
    BigIntegerField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.assignment import Assignment

class BaseModel(Model):
    class Meta:
        database = database

class AssignmentFile(BaseModel):
    id = AutoField()
    assignment = ForeignKeyField(Assignment, backref='files', on_delete='CASCADE', on_update='CASCADE', column_name='assignment_id')
    file_id = BigIntegerField()
    created_at = DateTimeField()

    class Meta:
        table_name = "assignments_files"
        indexes = (
            (('assignment', 'file_id'), True),
        )
