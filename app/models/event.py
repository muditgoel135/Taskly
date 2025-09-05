from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from ..extensions import db

class Event(db.Model):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_at: Mapped[datetime | None]
    end_at: Mapped[datetime | None]
    location: Mapped[str | None]
