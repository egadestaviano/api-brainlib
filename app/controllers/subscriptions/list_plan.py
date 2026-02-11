from flask import jsonify
from app.models.subscription import Plan

def list_plan_handler():
    """Return list of all subscription plans"""
    plans = list(Plan.select())
    data = [
        {
            "id": plan.id,
            "name": plan.name,
            "description": plan.description,
            "price": str(plan.price),
            "stripe_price_id": plan.stripe_price_id,
        }
        for plan in plans
    ]
    return jsonify(data), 200
