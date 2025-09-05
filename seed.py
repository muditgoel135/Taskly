from __future__ import annotations
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.task import Task
from app.services.security import hash_password

app = create_app()
with app.app_context():
    db.drop_all(); db.create_all()
    u = User(email="student@example.com", password_hash=hash_password("pass"))
    db.session.add(u)
    db.session.commit()
    db.session.add_all([
        Task(owner_id=u.id, title="Math homework", priority=2),
        Task(owner_id=u.id, title="Science notes", priority=1),
    ])
    db.session.commit()
    print("Seeded: student@example.com / pass")
