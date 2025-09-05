from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("users", "users", description="Users")

@blp.get("/")
def list_users():
    return {"items": []}
