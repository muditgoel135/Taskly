# Task Planner – Design 1

**Stack**: Flask 3, SQLAlchemy 2, Alembic, Flask-Smorest + Marshmallow, JWT, Socket.IO, Celery + Redis, Tailwind (CDN), HTMX + Alpine, Postgres.

## Quick start (Docker)

```bash
git clone <this repo>
cd student-task-planner
cp .env.example .env
docker compose up --build -d
# wait a few seconds for db, then run migrations
docker compose exec web alembic upgrade head
# (optional) seed demo data inside container
docker compose exec web python seed.py
```

Open [http://localhost:8000](http://localhost:8000)

### First login

Register via `POST /api/v1/auth/register` or call `seed.py` and then `POST /api/v1/auth/login`.

## What’s implemented now

* Dark theme **everywhere**, Arial font, medium density, minimal imagery.
* Navigation: left **sidebar** + **tabs** (grouping primitive via Alpine state).
* **Homepage** widgets: AI prompt bar, Quick-add Task/Event, Upcoming, Frequently visited.
* API v1 with JWT auth; Tasks/Events CRUD; AI `/assist` & `/schedule` (LOCAL stub).
* Celery + Redis wired; Socket.IO for live events (sample channels).
* PWA basics: manifest + service worker for offline caching.
* Alembic initial migration for all core tables.

## Run locally without Docker

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export FLASK_ENV=development
# ensure Postgres & Redis are available (see .env)
flask --app app:create_app run
```

## Testing

```bash
pytest -q
```

## Notes & Next steps

* Replace LOCAL AI with OpenAI when `LLM_PROVIDER=OPENAI` and key set.
* Build Pages editor (bold/italic/underline, lists, tables, equations) – start with a simple toolbar and contenteditable, then enhance.
* Implement DB views (table, calendar, list, gallery, charts) and embed blocks on Pages.
* Web Push (VAPID) service + Chrome extension companion for distraction blocking.
* Stripe checkout + webhook for ₹200/month Premium gating advanced features.
