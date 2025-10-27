# directories.py
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    current_app,
)
from models import db, Page
import bleach, json
from datetime import datetime, timezone

pages_bp = Blueprint("pages", __name__)

# Tweak bleach policy to your needs
ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "h1",
    "h2",
    "h3",
    "pre",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
]
ALLOWED_ATTRS = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "img": ["src", "alt", "width", "height"],
    "*": ["style"],
}


@pages_bp.route("/")
def index():
    """Render the home page with a list of pages."""
    pages = Page.query.order_by(Page.updated_at.desc()).all()
    recent_pages = pages[:5]  # for example, show the 5 most recently updated pages
    return render_template("index.html", pages=pages, recent_pages=recent_pages)


@pages_bp.route("/new", methods=["GET", "POST"])
def new_page():
    if request.method == "POST":
        title = request.form.get("title", "Untitled Page")
        p = Page(title=title, content="<p>Start writing...</p>")
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("pages.edit_page", page_id=p.id))

    # GET -> render the form to create a new page
    return render_template("new_page.html")


@pages_bp.route("/page/<int:page_id>/delete", methods=["POST"])
def delete_page(page_id):
    p = Page.query.get_or_404(page_id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("pages.index"))


@pages_bp.route("/page/<int:page_id>")
def edit_page(page_id):
    p = Page.query.get_or_404(page_id)
    return render_template("editor.html", page=p)


@pages_bp.route("/pages")
def list_pages():
    pages = Page.query.order_by(Page.updated_at.desc()).all()
    return render_template("pages.html", pages=pages)


@pages_bp.route("/api/save/<int:page_id>", methods=["POST"])
def api_save(page_id):
    """API endpoint to save page content via AJAX."""
    p = Page.query.get_or_404(page_id)

    # be tolerant of missing/invalid JSON
    data = request.get_json(silent=True) or {}

    # extract fields safely
    raw_title = data.get("title") or ""
    raw_html = data.get("content_html") or ""
    delta = data.get("delta", None)

    # sanitize
    cleaned_title = bleach.clean(raw_title, tags=[], attributes={}, strip=True)
    if not cleaned_title:
        cleaned_title = "Untitled Page"

    cleaned_html = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

    # assign
    p.title = cleaned_title
    p.content = cleaned_html

    # store delta if serializable, else null it
    if delta is None:
        p.content_delta = None
    else:
        try:
            p.content_delta = json.dumps(delta, ensure_ascii=False)
        except (TypeError, ValueError):
            p.content_delta = None

    # timestamp (timezone-aware) and persist
    p.updated_at = datetime.now(timezone.utc)

    try:
        db.session.add(p)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        # log exc on server side if you have logging configured
        return jsonify(success=False, error="failed_to_save"), 500

    return jsonify(success=True, updated_at=p.updated_at.isoformat())

@pages_bp.route("/sidebar")
def sidebar():
    """Render the sidebar partial."""
    pages = Page.query.order_by(Page.updated_at.desc()).all()
    return render_template("sidebar.html", pages=pages)