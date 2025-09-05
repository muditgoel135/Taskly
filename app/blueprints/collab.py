from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("collab", "collab", description="Collaboration")

@blp.get("/rooms")
def rooms():
    return {"items": []}
