from flask import request, jsonify, redirect
from itsdangerous import BadSignature
import os

from app.config import FRONTEND_BASE_URL
from app.models.subscription import Subscription
from itsdangerous import URLSafeSerializer

serializer = URLSafeSerializer(os.getenv("SECRET_KEY"), salt="checkout-token")

def checkout_cancel_handler():
    sub_id = request.args.get("sub_id")
    token = request.args.get("t")
    try:
        data = serializer.loads(token)
    except BadSignature:
        return jsonify({"error": "invalid token"}), 400

    if int(data.get("sub_id")) != int(sub_id):
        return jsonify({"error": "token mismatch"}), 400

    subscription = Subscription.get_or_none(Subscription.id == sub_id)
    if subscription:
        subscription.status = "canceled"
        subscription.save()

    return redirect(f"{FRONTEND_BASE_URL}/subscription?status=canceled", code=302)
