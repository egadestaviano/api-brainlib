from flask import request, jsonify
from datetime import datetime, timedelta
import stripe

from app.models.user import User
from app.models.subscription import Subscription, Plan
from app.mailer import send_subscription_email
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET

stripe.api_key = STRIPE_SECRET_KEY

def webhook_subscription_handler():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid Stripe signature"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_email")
        subscription_id = session.get("subscription")
        checkout_id = session.get("id")

        user = User.get_or_none(User.email == email)
        if not user:
            return jsonify({"error": f"User not found for email {email}"}), 404

        line_items = stripe.checkout.Session.list_line_items(checkout_id)
        if not line_items.data:
            return jsonify({"error": "No line items found"}), 400

        price_id = line_items.data[0].price.id

        plan = Plan.get_or_none(Plan.stripe_price_id == price_id)
        if not plan:
            return jsonify({"error": f"Plan not found for price_id {price_id}"}), 404

        subscription = Subscription.get_or_none(
            Subscription.user == user,
            Subscription.plan == plan
        )
        if not subscription:
            subscription = Subscription.create(
                user=user,
                plan=plan,
                stripe_subscription_id=subscription_id,
                status="active",
                started_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30),
            )
        else:
            subscription.stripe_subscription_id = subscription_id
            subscription.status = "active"
            subscription.started_at = datetime.utcnow()
            subscription.expires_at = datetime.utcnow() + timedelta(days=30)
            subscription.save()

        try:
            send_subscription_email(user.email, plan.name)
        except Exception as e:
            print(f"❌ Failed Send email to {user.email}: {e}")

    elif event["type"] == "invoice.payment_failed":
        print("⚠️ Payment failed event send")

    return jsonify({"status": "success"}), 200
