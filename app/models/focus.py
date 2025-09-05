from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from ..extensions import db

class FocusSession(db.Model):
    __tablename__ = "focus_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    minutes: Mapped[int] = mapped_column(Integer, default=25)
