from __future__ import annotations
from flask_smorest import Blueprint, abort
from flask import request
from flask_jwt_extended import jwt_required
from ..services.ai_service import AIService
from ..services.schedule_service import ScheduleService
from flask import current_app

blp = Blueprint("ai", "ai", description="AI endpoints")

@blp.post("/assist")
@jwt_required(optional=True)
def assist():
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    s = current_app.settings
    ai = AIService(provider=s.LLM_PROVIDER, api_key=s.OPENAI_API_KEY)
    return {"text": ai.assist(prompt)}

@blp.post("/schedule")
@jwt_required(optional=True)
def schedule():
    data = request.get_json() or {}
    s = current_app.settings
    ai = AIService(provider=s.LLM_PROVIDER, api_key=s.OPENAI_API_KEY)
    svc = ScheduleService(ai)
    return svc.generate(data)
