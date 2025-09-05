from __future__ import annotations
from marshmallow import Schema, fields

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    start_at = fields.DateTime(allow_none=True)
    end_at = fields.DateTime(allow_none=True)
    location = fields.Str(allow_none=True)

class EventCreateSchema(Schema):
    title = fields.Str(required=True)
    start_at = fields.DateTime(allow_none=True)
    end_at = fields.DateTime(allow_none=True)
    location = fields.Str(allow_none=True)
