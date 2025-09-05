from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("notifications", "notifications", description="Notifications")

@blp.post("/subscribe")
def save_push_subscription():
    # Store browser push subscription (stub)
    return {"ok": True}
