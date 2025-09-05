from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("habits", "habits", description="Habits")

@blp.get("/")
def list_habits():
    return {"items": []}
