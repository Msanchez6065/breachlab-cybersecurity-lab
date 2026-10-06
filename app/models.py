"""Database models used by BreachLab."""

from app.database import db


class User(db.Model):
    """A lab user; only password hashes are stored."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), nullable=False)