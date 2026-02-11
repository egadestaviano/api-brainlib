from peewee import (
    Model,
    AutoField,
    CharField,
    BooleanField,
    DateTimeField,
    ForeignKeyField,
    CompositeKey,
)
from app.db import database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    id = AutoField()
    email = CharField(max_length=255, unique=True, index=True)
    password_hash = CharField(max_length=255)
    is_active = BooleanField(default=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "users"


class Role(BaseModel):
    id = AutoField()
    name = CharField(max_length=64, unique=True)
    description = CharField(max_length=255, null=True)

    class Meta:
        table_name = "roles"


class Permission(BaseModel):
    id = AutoField()
    name = CharField(max_length=64, unique=True)
    description = CharField(max_length=255, null=True)

    class Meta:
        table_name = "permissions"


class RolePermission(Model):
    role = ForeignKeyField(Role, backref="permissions", on_delete="CASCADE")
    permission = ForeignKeyField(Permission, backref="roles", on_delete="CASCADE")

    class Meta:
        database = database
        table_name = "role_permissions"
        primary_key = CompositeKey("role", "permission")


class UserRole(Model):
    user = ForeignKeyField(User, backref="roles", on_delete="CASCADE")
    role = ForeignKeyField(Role, backref="users", on_delete="CASCADE")

    class Meta:
        database = database
        table_name = "user_roles"
        primary_key = CompositeKey("user", "role")
