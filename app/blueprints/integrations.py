from __future__ import annotations
from flask_smorest import Blueprint

blp = Blueprint("integrations", "integrations", description="Integrations (stubs)")

@blp.get("/providers")
def providers():
    return {"providers": ["google_calendar", "ics", "school_portal"]}
