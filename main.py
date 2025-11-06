# Import necessary modules
from flask import Flask, current_app
import os
from models import db, Page
import traceback

# Set up directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskly.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

# initialize db with app
db.init_app(app)


@app.context_processor
def inject_pages():
    """
    Makes `pages` available in all templates (sidebar included).
    If an error happens, log it so it doesn't silently return [].
    """
    try:
        pages = Page.query.order_by(Page.updated_at.desc()).all()
        return dict(pages=pages)
    except Exception as e:
        # log the full traceback for debugging
        current_app.logger.error("inject_pages() failed: %s", e)
        current_app.logger.error(traceback.format_exc())
        # return an empty list so pages is defined and templates don't crash
        return dict(pages=[])


# register the blueprint AFTER db.init_app
from directories import pages_bp

app.register_blueprint(pages_bp)

# create tables on startup (dev convenience)
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
