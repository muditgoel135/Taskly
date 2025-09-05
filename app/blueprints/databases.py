from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("databases", "databases", description="Databases/API")

@blp.get("/")
def list_dbs():
    return {"items": []}
