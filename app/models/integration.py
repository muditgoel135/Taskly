from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from ..extensions import db

class Integration(db.Model):
    __tablename__ = "integrations"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(64))  # google_calendar, school_portal, ics
    access_token: Mapped[str | None]
