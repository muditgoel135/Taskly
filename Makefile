.PHONY: dev up down migrate seed

dev:
FLASK_ENV=development flask run --app app:create_app --debug

up:
docker compose up --build

down:
docker compose down -v

migrate:
alembic upgrade head

seed:
python seed.py
