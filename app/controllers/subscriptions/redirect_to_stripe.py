import stripe
from flask import request, jsonify, redirect
from itsdangerous import BadSignature
import os

from app.config import STRIPE_SECRET_KEY
from app.models.subscription import Subscription
from itsdangerous import URLSafeSerializer

stripe.api_key = STRIPE_SECRET_KEY
serializer = URLSafeSerializer(os.getenv("SECRET_KEY"), salt="checkout-token")

def redirect_to_stripe_handler(sub_id):
    token = request.args.get("t")
    if not token:
        return jsonify({"error": "missing token"}), 400

    try:
        data = serializer.loads(token)
    except BadSignature:
        return jsonify({"error": "invalid token"}), 400

    if data.get("sub_id") != int(sub_id):
        return jsonify({"error": "token does not match subscription"}), 400

    subscription = Subscription.get_or_none(Subscription.id == sub_id)
    if not subscription:
        return jsonify({"error": "subscription not found"}), 404

    try:
        session = stripe.checkout.Session.retrieve(subscription.stripe_subscription_id)
    except Exception as e:
        return jsonify({"error": f"stripe session retrieve error: {e}"}), 500

    return redirect(session.url, code=302)
