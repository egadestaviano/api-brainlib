from peewee import (
    Model,
    AutoField,
    BigIntegerField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.submission import Submission

class BaseModel(Model):
    class Meta:
        database = database

class SubmissionFile(BaseModel):
    id = AutoField()
    submission = ForeignKeyField(Submission, backref='files', on_delete='CASCADE', on_update='CASCADE', column_name='submission_id')
    file_id = BigIntegerField()
    created_at = DateTimeField()

    class Meta:
        table_name = "submission_files"
        indexes = (
            (('submission', 'file_id'), True),
        )
