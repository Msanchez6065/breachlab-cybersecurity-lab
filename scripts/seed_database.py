"""Create the database table and insert fake users for local lab use."""

import secrets

from werkzeug.security import generate_password_hash

from app import create_app
from app.database import db
from app.models import User

app = create_app()

FAKE_USERS = (
    ("lab_employee", "employee"),
    ("lab_manager", "manager"),
    ("lab_admin", "administrator"),
)


def seed_database():
    with app.app_context():
        db.create_all()
        added = 0
        for username, role in FAKE_USERS:
            if db.session.query(User).filter_by(username=username).first():
                continue
            db.session.add(
                User(
                    username=username,
                    password_hash=generate_password_hash(secrets.token_urlsafe(24)),
                    role=role,
                )
            )
            added += 1
        db.session.commit()
        print(f"Database ready. Added {added} fake test user(s).")


if __name__ == "__main__":
    seed_database()