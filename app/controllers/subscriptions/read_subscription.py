from flask import request, jsonify
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionSchema

read_schema = SubscriptionSchema(many=True)

def read_subscription_handler():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    query = Subscription.select().offset(offset).limit(per_page)
    total = Subscription.select().count()

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "data": read_schema.dump(query)
    }), 200
