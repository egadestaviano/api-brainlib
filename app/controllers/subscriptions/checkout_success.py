import stripe
from flask import request, jsonify, redirect
from datetime import datetime, timedelta
from itsdangerous import BadSignature
import os

from app.config import STRIPE_SECRET_KEY, FRONTEND_BASE_URL
from app.mailer import send_subscription_email
from app.models.subscription import Subscription, Plan
from itsdangerous import URLSafeSerializer

stripe.api_key = STRIPE_SECRET_KEY
serializer = URLSafeSerializer(os.getenv("SECRET_KEY"), salt="checkout-token")

def checkout_success_handler():
    session_id = request.args.get("session_id")
    sub_id = request.args.get("sub_id")
    token = request.args.get("t")

    if not session_id or not sub_id or not token:
        return jsonify({"error": "missing parameters"}), 400

    try:
        data = serializer.loads(token)
    except BadSignature:
        return jsonify({"error": "invalid token"}), 400

    if int(data.get("sub_id")) != int(sub_id):
        return jsonify({"error": "token mismatch"}), 400

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        return jsonify({"error": f"stripe retrieve error: {e}"}), 500

    if session.payment_status not in ("paid", "no_payment_required"):
        return redirect(f"{FRONTEND_BASE_URL}/subscription?status=failed")

    stripe_sub_id = session.get("subscription")
    stripe_subscription_obj = None
    if stripe_sub_id:
        stripe_subscription_obj = stripe.Subscription.retrieve(stripe_sub_id)

    subscription = Subscription.get_or_none(Subscription.id == sub_id)
    if not subscription:
        return jsonify({"error": "subscription row not found"}), 404

    if stripe_subscription_obj:
        start_ts = stripe_subscription_obj.get("current_period_start")
        end_ts = stripe_subscription_obj.get("current_period_end")

        subscription.stripe_subscription_id = stripe_subscription_obj["id"]
        subscription.status = "active"
        subscription.started_at = datetime.utcfromtimestamp(start_ts) if start_ts else datetime.utcnow()
        subscription.expires_at = datetime.utcfromtimestamp(end_ts) if end_ts else datetime.utcnow() + timedelta(days=30)
    else:
        subscription.status = "active"
        subscription.started_at = datetime.utcnow()
        subscription.expires_at = datetime.utcnow() + timedelta(days=30)

    subscription.save()
    
    plan_name = subscription.plan.name if subscription.plan else "Unknown Plan"
    send_subscription_email(subscription.user.email, plan_name)

    return redirect(f"{FRONTEND_BASE_URL}/subscription?status=success&sub_id={subscription.id}", code=302)
