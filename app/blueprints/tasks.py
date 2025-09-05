from __future__ import annotations
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.task import Task
from ..schemas.task import TaskSchema, TaskCreateSchema

blp = Blueprint("tasks", "tasks", description="Tasks CRUD")

@blp.get("/")
@jwt_required()
@blp.response(200, TaskSchema(many=True))
def list_tasks():
    uid = get_jwt_identity()
    items = db.session.query(Task).filter_by(owner_id=uid).order_by(Task.due_at).all()
    return items

@blp.post("/")
@jwt_required()
@blp.arguments(TaskCreateSchema)
@blp.response(201, TaskSchema)
def create_task(body):
    uid = get_jwt_identity()
    t = Task(owner_id=uid, **body)
    db.session.add(t)
    db.session.commit()
    return t

@blp.delete("/<int:task_id>")
@jwt_required()
@blp.response(204)
def delete_task(task_id: int):
    uid = get_jwt_identity()
    t = db.session.get(Task, task_id)
    if not t or t.owner_id != uid:
        abort(404, message="task not found")
    db.session.delete(t)
    db.session.commit()
    return "", 204
