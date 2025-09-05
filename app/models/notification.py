from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey
from ..extensions import db

class Notification(db.Model):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    channel: Mapped[str] = mapped_column(String(32))  # inapp, push, email
    payload: Mapped[str] = mapped_column(String(1024))
    sent: Mapped[bool] = mapped_column(Boolean, default=False)
