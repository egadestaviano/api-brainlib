import stripe
from flask import request, jsonify, redirect
from datetime import datetime, timedelta
from itsdangerous import URLSafeSerializer
import os

from app.config import STRIPE_SECRET_KEY, BACKEND_BASE_URL
from app.utils.auth import get_user_from_token
from app.models.subscription import Subscription, Plan
from app.schemas.subscription import SubscriptionSchema

stripe.api_key = STRIPE_SECRET_KEY
serializer = URLSafeSerializer(os.getenv("SECRET_KEY"), salt="checkout-token")
create_schema = SubscriptionSchema()


def create_subscription_handler():
    user, profile, err = get_user_from_token()
    if err:
        return err

    payload = request.get_json(silent=True) or {}
    plan_id = payload.get("plan_id")
    if not plan_id:
        return jsonify({"error": "plan_id is required"}), 400

    plan = Plan.get_or_none(Plan.id == plan_id)
    if not plan:
        return jsonify({"error": "Plan not found"}), 404

    if plan.price == 0:
        subscription = Subscription.create(
            user=user,
            plan=plan,
            stripe_subscription_id="free",
            status="active",
            started_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=365),
        )

        return jsonify({
            "redirect_path": f"/subscription?status=success&sub_id={subscription.id}",
            "checkout_url": f"/subscription?status=success&sub_id={subscription.id}"
        }), 201

    subscription = Subscription.create(
        user=user,
        plan=plan,
        stripe_subscription_id="",
        status="pending",
        started_at=datetime.utcnow(),
        expires_at=datetime.utcnow(),
    )

    token_payload = {"sub_id": subscription.id, "user_id": user.id}
    token = serializer.dumps(token_payload)

    success_url = f"{BACKEND_BASE_URL}/api/subscriptions/checkout-success?session_id={{CHECKOUT_SESSION_ID}}&sub_id={subscription.id}&t={token}"
    cancel_url = f"{BACKEND_BASE_URL}/api/subscriptions/checkout-cancel?sub_id={subscription.id}&t={token}"

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(subscription.id),
        customer_email=user.email,
        metadata={"sub_id": str(subscription.id), "user_id": str(user.id)},
    )

    subscription.stripe_subscription_id = session.id
    subscription.save()

    redirect_path = f"/api/subscriptions/redirect/{subscription.id}?t={token}"

    return jsonify({
        "redirect_path": redirect_path,
        "checkout_url": session.url
    }), 201
