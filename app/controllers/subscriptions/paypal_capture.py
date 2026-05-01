import requests
from flask import request, jsonify
from datetime import datetime, timedelta
from app.config import PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_MODE
from app.models.subscription import Subscription
from app.controllers.subscriptions.create_subscription import get_paypal_access_token

def paypal_capture_handler():
    payload = request.get_json(silent=True) or {}
    order_id = payload.get("order_id")
    sub_id = payload.get("sub_id")
    
    if not order_id or not sub_id:
        return jsonify({"error": "order_id and sub_id are required"}), 400
        
    subscription = Subscription.get_or_none(Subscription.id == sub_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404
        
    access_token = get_paypal_access_token()
    if not access_token:
        # Fallback for mock/testing if no credentials
        subscription.status = "active"
        subscription.started_at = datetime.utcnow()
        subscription.expires_at = datetime.utcnow() + timedelta(days=30)
        subscription.save()
        return jsonify({"message": "Subscription activated (mock)"}), 200

    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture" if PAYPAL_MODE == "sandbox" else f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    
    try:
        resp = requests.post(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get("status") == "COMPLETED":
            # Deactivate any previous active subscriptions for this user
            Subscription.update(status='inactive').where(
                (Subscription.user == subscription.user) & (Subscription.status == 'active')
            ).execute()

            duration_days = 365 if "Yearly" in subscription.plan.name else 30
            subscription.status = "active"
            subscription.started_at = datetime.utcnow()
            subscription.expires_at = datetime.utcnow() + timedelta(days=duration_days)
            subscription.save()
            return jsonify({"message": "Payment captured and subscription activated"}), 200
        else:
            return jsonify({"error": "Failed to capture payment", "details": data}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error during capture: {str(e)}"}), 500
