from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("goals", "goals", description="Goals")

@blp.get("/")
def list_goals():
    return {"items": []}
