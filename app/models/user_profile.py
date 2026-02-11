from peewee import (
    Model,
    AutoField,
    IntegerField,
    BigIntegerField,
    TextField,
    CharField,
    ForeignKeyField,
    DateTimeField,
)
from app.db import database
from app.models.user import User

class BaseModel(Model):
    class Meta:
        database = database

class UserProfile(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='profile', unique=True, on_delete='CASCADE', on_update='CASCADE')
    display_name = CharField(max_length=255, null=True)
    avatar_file_id = BigIntegerField(null=True)
    bio = TextField(null=True)
    extra = TextField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "user_profiles"
