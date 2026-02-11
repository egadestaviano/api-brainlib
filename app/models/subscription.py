from peewee import (
    Model, AutoField, CharField, ForeignKeyField, DateTimeField, DecimalField
)
from datetime import datetime
from app.db import database
from app.models.user import User


class BaseModel(Model):
    class Meta:
        database = database


class Plan(BaseModel):
    id = AutoField()
    name = CharField(max_length=64, unique=True)
    stripe_price_id = CharField(max_length=128)
    description = CharField(max_length=255, null=True)
    price = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "plans"


class Subscription(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="subscriptions", on_delete="CASCADE")
    plan = ForeignKeyField(Plan, backref="subscriptions", on_delete="CASCADE")
    stripe_subscription_id = CharField(max_length=128)
    status = CharField(max_length=64, default="active")
    started_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField()

    class Meta:
        table_name = "subscriptions"
