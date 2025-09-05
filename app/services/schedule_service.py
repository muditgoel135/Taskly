from __future__ import annotations
from typing import Any, Dict

from .ai_service import AIService

class ScheduleService:
    def __init__(self, ai: AIService):
        self.ai = ai

    def generate(self, payload: Dict[str, Any]):
        tasks = payload.get("tasks", [])
        prefs = payload.get("prefs", {})
        constraints = payload.get("constraints", {})
        return self.ai.schedule(tasks, prefs, constraints)
