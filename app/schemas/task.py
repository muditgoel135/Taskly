from __future__ import annotations
from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    due_at = fields.DateTime(allow_none=True)
    priority = fields.Int()
    done = fields.Bool()

class TaskCreateSchema(Schema):
    title = fields.Str(required=True)
    due_at = fields.DateTime(allow_none=True)
    priority = fields.Int(load_default=1)
