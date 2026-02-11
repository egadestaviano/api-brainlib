from marshmallow import Schema, fields


class PlanSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    stripe_price_id = fields.Str()
    description = fields.Str()
    price = fields.Float()


class SubscriptionSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(attribute="user.id")
    plan = fields.Nested(PlanSchema)
    stripe_subscription_id = fields.Str()
    status = fields.Str()
    started_at = fields.DateTime()
    expires_at = fields.DateTime()
