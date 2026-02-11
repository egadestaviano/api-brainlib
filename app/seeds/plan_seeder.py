from app.models.subscription import Plan
from decimal import Decimal

def seed_plans():
    plans_data = [
        {
            "name": "Free",
            "stripe_price_id": "free",
            "description": "Free plan for beginners. Access to basic features.",
            "price": Decimal("0.00"),
        },
        {
            "name": "Pro",
            "stripe_price_id": "price_1SKFOM4JZMFfFZZO5VagDuar",
            "description": "Pro plan with full feature access.",
            "price": Decimal("99.00"),
        },
        {
            "name": "Business",
            "stripe_price_id": "price_1SKFPw4JZMFfFZZOVYSZx3H2",
            "description": "Business plan with advanced features and priority support.",
            "price": Decimal("299.00"),
        },
    ]

    for plan_data in plans_data:
        plan, created = Plan.get_or_create(name=plan_data["name"])

        plan.stripe_price_id = plan_data["stripe_price_id"]
        plan.description = plan_data["description"]
        plan.price = plan_data["price"]
        plan.save()

        if created:
            print(f"✅ Plan '{plan.name}' has been created.")
        else:
            print(f"🔄 Plan '{plan.name}' has been updated.")
