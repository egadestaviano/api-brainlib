from flask import Blueprint

from app.controllers.subscriptions.create_subscription import create_subscription_handler
from app.controllers.subscriptions.read_subscription import read_subscription_handler
from app.controllers.subscriptions.webhook_subscription import webhook_subscription_handler
from app.controllers.subscriptions.list_plan import list_plan_handler
from app.controllers.subscriptions.read_current_subscription_handler import read_current_subscription_handler
from app.controllers.subscriptions.redirect_to_stripe import redirect_to_stripe_handler
from app.controllers.subscriptions.checkout_success import checkout_success_handler
from app.controllers.subscriptions.checkout_cancel import checkout_cancel_handler

subscription_bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


@subscription_bp.post("")
def create_subscription():
    """
    Create a subscription checkout session
    ---
    tags:
      - Subscriptions
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - plan_id
          properties:
            plan_id:
              type: integer
    responses:
      201:
        description: Checkout session created
      400:
        description: Bad Request
      404:
        description: User or Plan not found
    """
    return create_subscription_handler()


@subscription_bp.get("")
def list_subscriptions():
    """
    List subscriptions
    ---
    tags:
      - Subscriptions
    parameters:
      - in: query
        name: page
        type: integer
      - in: query
        name: per_page
        type: integer
    responses:
      200:
        description: OK
    """
    return read_subscription_handler()


@subscription_bp.get("/plans")
def list_plans():
    """
    List available subscription plans
    ---
    tags:
      - Subscriptions
    responses:
      200:
        description: OK
    """
    return list_plan_handler()


@subscription_bp.post("/webhook")
def stripe_webhook():
    """
    Stripe Webhook
    ---
    tags:
      - Subscriptions
    consumes:
      - application/json
    responses:
      200:
        description: OK
    """
    return webhook_subscription_handler()


@subscription_bp.get("/current")
def get_current_subscription():
    """
    Get current active subscription of logged-in user
    ---
    tags:
      - Subscriptions
    responses:
      200:
        description: OK
    """
    return read_current_subscription_handler()


# ===============================
# Checkout Tanpa Webhook
# ===============================

@subscription_bp.get("/redirect/<sub_id>")
def redirect_to_stripe(sub_id):
    """
    Redirect ke Stripe Checkout
    ---
    tags:
      - Subscriptions
    parameters:
      - in: path
        name: sub_id
        required: true
        type: integer
      - in: query
        name: t
        required: true
        type: string
    responses:
      302:
        description: Redirect ke Stripe Checkout
    """
    return redirect_to_stripe_handler(sub_id)


@subscription_bp.get("/checkout-success")
def checkout_success():
    """
    Handle success dari Stripe Checkout (tanpa webhook)
    ---
    tags:
      - Subscriptions
    parameters:
      - in: query
        name: session_id
        required: true
        type: string
      - in: query
        name: sub_id
        required: true
        type: integer
      - in: query
        name: t
        required: true
        type: string
    responses:
      302:
        description: Redirect ke halaman sukses di FE
    """
    return checkout_success_handler()


@subscription_bp.get("/checkout-cancel")
def checkout_cancel():
    """
    Handle cancel dari Stripe Checkout (tanpa webhook)
    ---
    tags:
      - Subscriptions
    parameters:
      - in: query
        name: sub_id
        required: true
        type: integer
      - in: query
        name: t
        required: true
        type: string
    responses:
      302:
        description: Redirect ke halaman gagal di FE
    """
    return checkout_cancel_handler()
