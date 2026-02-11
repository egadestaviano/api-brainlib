from peewee import (
    Model,
    BigIntegerField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class AIEdit(BaseModel):
    id = BigIntegerField(primary_key=True)
    target_table = CharField(max_length=255)
    target_id = BigIntegerField()
    original_content = TextField(null=True)
    edited_content = TextField(null=True)
    editor_service = CharField(max_length=64)
    user = ForeignKeyField(User, backref='ai_edits', null=True, on_delete='SET NULL', on_update='CASCADE', column_name='user_id')
    created_at = DateTimeField()

    class Meta:
        table_name = "ai_edits"
