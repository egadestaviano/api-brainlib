from peewee import (
    Model,
    BigIntegerField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class AuditLog(BaseModel):
    id = BigIntegerField(primary_key=True)
    actor = ForeignKeyField(User, backref='audit_logs', null=True, on_delete='SET NULL', on_update='CASCADE', column_name='actor_id')
    action = CharField(max_length=64)
    object_type = CharField(max_length=64)
    object_id = BigIntegerField(null=True)
    details = TextField(null=True)
    created_at = DateTimeField()

    class Meta:
        table_name = "audit_logs"
