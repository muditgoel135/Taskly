from __future__ import annotations
from flask_jwt_extended import get_jwt

ROLE = {
    "student": 10,
    "parent": 20,
    "teacher": 30,
    "admin": 100,
}

def require_role(min_role: str) -> bool:
    claims = get_jwt()
    role = claims.get("role", "student")
    return ROLE.get(role, 0) >= ROLE.get(min_role, 0)
