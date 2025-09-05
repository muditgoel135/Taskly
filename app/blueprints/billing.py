from __future__ import annotations
from flask_smorest import Blueprint, abort
from flask import current_app, request

blp = Blueprint("billing", "billing", description="Billing/Stripe test")

@blp.post("/create-checkout-session")
def create_checkout():
    if not current_app.config.get("STRIPE_SECRET_KEY"):
        abort(400, message="Stripe not configured")
    # Stub response; integrate stripe.checkout.Session.create later
    return {"url": "https://example.com/checkout/test"}
