from peewee import (
    Model,
    AutoField,
    BigIntegerField,
    CharField,
    TextField,
    IntegerField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class File(BaseModel):
    id = BigIntegerField(primary_key=True)
    owner = ForeignKeyField(User, backref='files', on_delete='CASCADE', on_update='CASCADE', column_name='owner_id')
    filename = CharField(max_length=255)
    mime_type = CharField(max_length=255, null=True)
    url = TextField(null=True)
    path = TextField(null=True)
    size_bytes = BigIntegerField(default=0)
    purpose = CharField(max_length=64, null=True)
    storage_backend = CharField(max_length=64, default='local')
    is_public = BooleanField(default=False)
    reference_count = IntegerField(default=0)
    metadata = TextField(null=True)
    uploaded_at = DateTimeField()

    class Meta:
        table_name = "files"
