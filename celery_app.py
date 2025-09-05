from __future__ import annotations
import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

celery_app = Celery("planner", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.conf.timezone = "Asia/Kolkata"

@celery_app.task
def send_notification(user_id: int, payload: dict):
    # Stub: push via websockets (or email)
    return {"ok": True, "user_id": user_id, "payload": payload}

@celery_app.task
def generate_schedule_job(payload: dict):
    # Could call AI service; return schedule
    return {"ok": True}
