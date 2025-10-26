import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_DIR = os.path.join(BASE_DIR, "data")
PAGES_DIR = os.path.join(DATA_DIR, "pages")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# basic configuration variables
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskly.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tasks")
def tasks():
    pass  # Placeholder for tasks route implementation


@app.route("/events")
def events():
    pass  # Placeholder for events route implementation


@app.route("/add-task", methods=["POST"])
def add_task():
    pass  # Placeholder for add_task route implementation
    return redirect("/")


@app.route("/add-event", methods=["POST"])
def add_event():
    pass  # Placeholder for add_event route implementation
    return redirect("/")
