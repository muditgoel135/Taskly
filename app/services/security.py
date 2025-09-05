from __future__ import annotations
from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(raw: str) -> str:
    return ph.hash(raw)

def verify_password(hashv: str, raw: str) -> bool:
    try:
        ph.verify(hashv, raw)
        return True
    except Exception:
        return False
