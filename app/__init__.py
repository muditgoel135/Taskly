from __future__ import annotations
import logging
import os
import uuid
from flask import Flask, g, jsonify, render_template, request
from .extensions import db, ma, jwt, socketio, cache, limiter, csrf, smorest_api, talisman
from .settings import Settings
from .config import BaseConfig, DevConfig, ProdConfig
from .sockets import register_socket_events

# Blueprints
from .blueprints.auth import blp as auth_blp
from .blueprints.tasks import blp as tasks_blp
from .blueprints.events import blp as events_blp
from .blueprints.pages import ui as pages_ui_bp, blp as pages_api_blp
from .blueprints.databases import blp as db_blp
from .blueprints.ai import blp as ai_blp
from .blueprints.integrations import blp as integrations_blp
from .blueprints.notifications import blp as notif_blp
from .blueprints.users import blp as users_blp
from .blueprints.habits import blp as habits_blp
from .blueprints.goals import blp as goals_blp
from .blueprints.collab import blp as collab_blp
from .blueprints.billing import blp as billing_blp
from .blueprints.admin import blp as admin_blp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Load environment settings via pydantic
    settings = Settings()  # reads .env automatically
    app.config.from_object(BaseConfig(settings))
    if settings.FLASK_ENV == "development":
        app.config.from_object(DevConfig(settings))
    elif settings.FLASK_ENV == "production":
        app.config.from_object(ProdConfig(settings))

    # Attach settings for easy access
    app.settings = settings  # type: ignore[attr-defined]

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Talisman (CSP/HSTS)
    talisman.init_app(
        app,
        content_security_policy={
            "default-src": "'self'",
            # Allow HTMX/Alpine/Tailwind CDN, websockets
            "script-src": "'self' https://cdn.tailwindcss.com https://unpkg.com 'unsafe-inline'",
            "style-src": "'self' 'unsafe-inline'",
            "img-src": "'self' data:",
            "connect-src": "'self' ws: wss:",
        },
        force_https=app.config.get("SESSION_COOKIE_SECURE", False),
    )

    # Smorest API
    smorest_api.init_app(app)

    # Register API blueprints under /api/v1
    smorest_api.register_blueprint(auth_blp, url_prefix="/api/v1/auth")
    smorest_api.register_blueprint(users_blp, url_prefix="/api/v1/users")
    smorest_api.register_blueprint(tasks_blp, url_prefix="/api/v1/tasks")
    smorest_api.register_blueprint(events_blp, url_prefix="/api/v1/events")
    smorest_api.register_blueprint(db_blp, url_prefix="/api/v1/databases")
    smorest_api.register_blueprint(ai_blp, url_prefix="/api/v1/ai")
    smorest_api.register_blueprint(integrations_blp, url_prefix="/api/v1/integrations")
    smorest_api.register_blueprint(notif_blp, url_prefix="/api/v1/notifications")
    smorest_api.register_blueprint(habits_blp, url_prefix="/api/v1/habits")
    smorest_api.register_blueprint(goals_blp, url_prefix="/api/v1/goals")
    smorest_api.register_blueprint(collab_blp, url_prefix="/api/v1/collab")
    smorest_api.register_blueprint(billing_blp, url_prefix="/api/v1/billing")
    smorest_api.register_blueprint(admin_blp, url_prefix="/api/v1/admin")

    # UI blueprint(s)
    app.register_blueprint(pages_ui_bp)

    # Socket.IO w/ Redis message queue
    socketio.init_app(app, message_queue=app.config["SOCKETIO_REDIS"], cors_allowed_origins="*")
    register_socket_events(socketio)

    # Request ID & JSON logging
    @app.before_request
    def before_request():
        g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))

    @app.after_request
    def after_request(response):
        response.headers["X-Request-Id"] = g.get("request_id", "-")
        app.logger.info(
            {
                "request_id": g.get("request_id"),
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "remote_addr": request.remote_addr,
            }
        )
        return response

    # Health endpoints
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/readiness")
    def readiness():
        try:
            db.session.execute(db.text("SELECT 1"))
            return {"status": "ready"}
        except Exception as e:
            return jsonify({"status": "degraded", "error": str(e)}), 503

    # Homepage (dark, sidebar + tabs + widgets)
    @app.get("/")
    def home():
        from .models.task import Task
        from .models.event import Event
        upcoming_tasks = Task.query.order_by(Task.due_at.asc()).limit(5).all()
        upcoming_events = Event.query.order_by(Event.start_at.asc()).limit(5).all()
        return render_template("home.html", tasks=upcoming_tasks, events=upcoming_events)

    return app
