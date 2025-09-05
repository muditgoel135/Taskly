from __future__ import annotations
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.event import Event
from ..schemas.event import EventSchema, EventCreateSchema

blp = Blueprint("events", "events", description="Events CRUD")

@blp.get("/")
@jwt_required()
@blp.response(200, EventSchema(many=True))
def list_events():
    uid = get_jwt_identity()
    items = db.session.query(Event).filter_by(owner_id=uid).order_by(Event.start_at).all()
    return items

@blp.post("/")
@jwt_required()
@blp.arguments(EventCreateSchema)
@blp.response(201, EventSchema)
def create_event(body):
    uid = get_jwt_identity()
    e = Event(owner_id=uid, **body)
    db.session.add(e)
    db.session.commit()
    return e
