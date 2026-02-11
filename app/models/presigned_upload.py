from peewee import (
    Model,
    BigIntegerField,
    CharField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class PresignedUpload(BaseModel):
    id = BigIntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='presigned_uploads', on_delete='CASCADE', on_update='CASCADE', column_name='user_id')
    key = CharField(max_length=255, unique=True)
    mime_type = CharField(max_length=255, null=True)
    filename = CharField(max_length=255, null=True)
    expires_at = DateTimeField()
    completed = BooleanField(default=False)
    created_at = DateTimeField()

    class Meta:
        table_name = "presigned_uploads"
