from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    ForeignKeyField,
    DateTimeField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class LmsClass(BaseModel):
    id = AutoField()
    title = CharField(max_length=255)
    description = TextField(null=True)
    code = CharField(max_length=64, unique=True)
    creator = ForeignKeyField(User, backref='classes', on_delete='CASCADE', on_update='CASCADE', column_name='creator_id')
    visibility = CharField(max_length=20, default='private')
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "classes"
