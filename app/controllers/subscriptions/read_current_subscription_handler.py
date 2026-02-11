from flask import jsonify
from app.utils.auth import get_user_from_token
from app.models.subscription import Subscription, Plan
from app.models.user import User

def read_current_subscription_handler():
    user, profile, error = get_user_from_token()
    if error:
        return error

    subscription = (
        Subscription
        .select(Subscription, Plan, User)
        .join(Plan, on=(Subscription.plan == Plan.id))
        .join(User, on=(Subscription.user == User.id))
        .where(
            (Subscription.user == user.id) &
            (Subscription.status == "active")
        )
        .order_by(Subscription.started_at.desc())
        .first()
    )

    if not subscription:
        return jsonify({"subscription": None, "message": "No active subscription"}), 200

    return jsonify({
        "id": subscription.id,
        "user_id": subscription.user.id,
        "user_email": subscription.user.email,
        "plan_id": subscription.plan.id,
        "plan_name": subscription.plan.name,
        "plan_price": str(subscription.plan.price),
        "status": subscription.status,
        "started_at": subscription.started_at.isoformat(),
        "expires_at": subscription.expires_at.isoformat(),
    }), 200
