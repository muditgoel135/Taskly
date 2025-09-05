from __future__ import annotations
from typing import Any, Dict, List
import datetime as dt

class AIService:
    def __init__(self, provider: str = "LOCAL", api_key: str | None = None):
        self.provider = provider
        self.api_key = api_key

    def assist(self, prompt: str) -> str:
        if self.provider == "OPENAI" and self.api_key:
            # Placeholder: wire an OpenAI call here later.
            pass
        # Local stub
        return (
            "Here are actionable subtasks and priorities based on your prompt.\n"
            "1) Break it down by due date. 2) Estimate durations. 3) Slot into study windows."
        )

    def schedule(self, tasks: List[Dict[str, Any]], prefs: Dict[str, Any], constraints: Dict[str, Any]):
        # Very simple local scheduler stub
        start = prefs.get("start_hour", 16)
        end = prefs.get("end_hour", 21)
        today = dt.datetime.now().date()
        blocks = []
        cur = dt.datetime.combine(today, dt.time(hour=start))
        for t in sorted(tasks, key=lambda x: (x.get("due"), -x.get("priority", 1))):
            dur = int(t.get("duration", 30))
            finish = cur + dt.timedelta(minutes=dur)
            if finish.time() > dt.time(hour=end):
                cur = dt.datetime.combine(today + dt.timedelta(days=1), dt.time(hour=start))
                finish = cur + dt.timedelta(minutes=dur)
            blocks.append(
                {
                    "title": t.get("title"),
                    "start": cur.isoformat(),
                    "end": finish.isoformat(),
                    "notes": f"Focus block for {t.get('title')} with short breaks",
                }
            )
            cur = finish + dt.timedelta(minutes=int(prefs.get("break_min", 5)))
        return {
            "blocks": blocks,
            "conflicts": [],
            "notes": "This is a locally generated draft schedule; enable OPENAI for richer reasoning.",
        }
