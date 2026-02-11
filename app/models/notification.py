from peewee import (
    Model,
    BigIntegerField,
    CharField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    TextField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class Notification(BaseModel):
    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='notifications', on_delete='CASCADE', on_update='CASCADE', column_name='user_id')
    type = CharField(max_length=64)
    payload = TextField(null=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField()

    class Meta:
        table_name = "notifications"
