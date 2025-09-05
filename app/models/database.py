from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, JSON, ForeignKey
from ..extensions import db

class Database(db.Model):
    __tablename__ = "databases"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    schema: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DatabaseItem(db.Model):
    __tablename__ = "database_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    database_id: Mapped[int] = mapped_column(ForeignKey("databases.id"), index=True)
    data: Mapped[dict] = mapped_column(JSON, default=dict)
