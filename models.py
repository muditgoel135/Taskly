# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create db object but do NOT bind to app here (avoids circular imports)
db = SQLAlchemy()


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default="Untitled Page")
    content = db.Column(
        db.Text, nullable=False, default=""
    )  # sanitized HTML for rendering
    content_delta = db.Column(
        db.Text, nullable=True
    )  # optional Quill delta JSON (string)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Page id={self.id} title={self.title}>"
