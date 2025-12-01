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

# Sanitization settings
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
    # Quill-specific / common HTML emitted by Quill formats
    "p",
    "div",
    "span",
    "br",
    "hr",
    "strong",  # bold (sometimes <b>)
    "b",
    "em",  # italic (sometimes <i>)
    "i",
    "u",  # underline
    "s",  # strike (sometimes <del> or <strike>)
    "del",
    "sub",
    "sup",
    "blockquote",
    "code",  # inline code
    "ol",
    "ul",
    "li",
    "input",  # checklist (checkbox)
    "figure",  # some editors wrap media
    "figcaption",
    "img",
    "iframe",  # video embeds (YouTube, etc.)
    "video",  # <video> tag (less common, but possible)
    "source",  # for <video>/<audio>
    "a",  # links
    "kbd",  # sometimes code-like formatting
    "svg",  # some embeds/icons (if you expect them)
    # keep the table tags you had (kept above)
]

ALLOWED_ATTRS = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    # image attributes Quill may include or that are safe for images/embed
    "img": [
        "src",
        "alt",
        "width",
        "height",
        "title",
        "loading",
        "referrerpolicy",
        "data-src",
        "class",
        "style",
    ],
    # anchor attributes
    "a": ["href", "title", "target", "rel", "class", "style"],
    # iframe/video/source attributes for embeds
    "iframe": [
        "src",
        "width",
        "height",
        "frameborder",
        "allow",
        "allowfullscreen",
        "loading",
        "referrerpolicy",
        "sandbox",
        "name",
        "class",
        "style",
    ],
    "video": [
        "src",
        "width",
        "height",
        "controls",
        "poster",
        "preload",
        "loop",
        "muted",
        "autoplay",
        "class",
        "style",
    ],
    "source": ["src", "type"],
    # input used for checklists
    "input": ["type", "checked", "disabled", "readonly", "class", "style"],
    # table related
    "table": [
        "class",
        "style",
        "summary",
        "width",
        "border",
        "cellpadding",
        "cellspacing",
    ],
    "td": ["colspan", "rowspan", "headers", "scope", "class", "style"],
    "th": ["colspan", "rowspan", "headers", "scope", "class", "style"],
    "tr": ["class", "style"],
    "thead": ["class", "style"],
    "tbody": ["class", "style"],
    # headings and other blocks (common attributes)
    "h1": ["id", "class", "style", "dir"],
    "h2": ["id", "class", "style", "dir"],
    "h3": ["id", "class", "style", "dir"],
    "pre": ["class", "style"],
    "code": ["class", "style"],
    "blockquote": ["cite", "class", "style", "dir"],
    # generic containers, inline elements
    "div": ["id", "class", "style", "dir"],
    "p": ["id", "class", "style", "dir"],
    "span": ["id", "class", "style", "dir", "data-value", "data-formula", "data-*"],
    "strong": ["class", "style"],
    "em": ["class", "style"],
    "u": ["class", "style"],
    "s": ["class", "style"],
    "sub": ["class", "style"],
    "sup": ["class", "style"],
    "ol": ["start", "class", "style"],
    "ul": ["class", "style"],
    "li": ["class", "style"],
    "figure": ["class", "style"],
    "figcaption": ["class", "style"],
    "kbd": ["class", "style"],
    # allow aria and role attributes for accessibility (optional but useful)
    "*": ["style", "class", "id", "dir", "role", "aria-label", "aria-hidden", "data-*"],
}


# Routes
@pages_bp.route("/")
def index():
    """Render the home page with a list of pages."""
    pages = Page.query.order_by(Page.updated_at.desc()).all()
    recent_pages = pages[:5]  # show the 5 most recently updated pages
    return render_template("index.html", pages=pages, recent_pages=recent_pages)


@pages_bp.route("/new", methods=["GET", "POST"])
def new_page():
    """Create a new page and redirect to its editor."""
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
    """Delete a page by its ID."""
    p = Page.query.get_or_404(page_id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("pages.index"))


@pages_bp.route("/page/<int:page_id>")
def edit_page(page_id):
    """Render the page editor for a given page ID."""
    p = Page.query.get_or_404(page_id)
    return render_template("editor.html", page=p)


@pages_bp.route("/pages")
def list_pages():
    """Render a list of all pages."""
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

    cleaned_html = bleach.clean(
        raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True
    )

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

@pages_bp.route("/events")
def events():
    """Render the events page."""
    return redirect(url_for("pages.index"))

@pages_bp.route("/tasks")
def tasks():
    """Render the tasks page."""
    return redirect(url_for("pages.index"))