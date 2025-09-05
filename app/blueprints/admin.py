from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("admin", "admin", description="Admin")

@blp.get("/stats")
def stats():
    return {"ok": True}
