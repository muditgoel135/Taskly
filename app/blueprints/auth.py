from __future__ import annotations
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..services.security import hash_password, verify_password

blp = Blueprint("auth", "auth", description="Auth endpoints")

@blp.post("/register")
@blp.response(201, schema=None)
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        abort(400, message="email and password required")
    if db.session.query(User).filter_by(email=email).first():
        abort(409, message="email exists")
    u = User(email=email, password_hash=hash_password(password))
    db.session.add(u)
    db.session.commit()
    return {"ok": True}

@blp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    user = db.session.query(User).filter_by(email=email).first()
    if not user or not verify_password(user.password_hash, password or ""):
        abort(401, message="invalid credentials")
    claims = {"role": user.role}
    return {
        "access": create_access_token(identity=user.id, additional_claims=claims),
        "refresh": create_refresh_token(identity=user.id, additional_claims=claims),
    }

@blp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    u = db.session.get(User, uid)
    return {"id": u.id, "email": u.email, "role": u.role}
