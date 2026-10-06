"""Application setup for the BreachLab web app."""

from flask import Flask, jsonify, render_template, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///breachlab.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)
    else:
        from app.database import get_database_url

        app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()

    db.init_app(app)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        message = None
        if request.method == "POST":
            message = "Authentication is not implemented in Version 0.1."
        # TODO (future lab exercises): add isolated training scenarios only
        # after their scope, safeguards, and remediation are documented.
        return render_template("login.html", message=message)

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(status="running", database="connected"), 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify(status="running", database="unavailable"), 503

    return app