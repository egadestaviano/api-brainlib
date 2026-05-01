from app.models.subscription import Plan
from decimal import Decimal

def seed_plans():
    plans_data = [
        {
            "name": "Starter",
            "stripe_price_id": "free",
            "description": "Perfect for individual educators getting started.",
            "price": Decimal("0.00"),
        },
        {
            "name": "Medium",
            "stripe_price_id": "price_medium",
            "description": "For growing teams and institutions.",
            "price": Decimal("10.00"),
        },
        {
            "name": "Enterprise",
            "stripe_price_id": "price_enterprise",
            "description": "Unlimited power for large organizations.",
            "price": Decimal("20.00"),
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
