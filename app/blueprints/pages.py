from __future__ import annotations
from flask import Blueprint, render_template
from flask_smorest import Blueprint as SBlueprint

ui = Blueprint("ui", __name__)
blp = SBlueprint("pages", "pages", description="Pages")

@ui.get("/pages/<int:page_id>")
def view_page(page_id: int):
    # Minimal stub page
    return render_template("home.html")
