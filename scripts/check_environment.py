"""Check required environment configuration and PostgreSQL connectivity."""

from sqlalchemy import text

from app import create_app
from app.database import db

app = create_app()


def check_environment():
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        print("PostgreSQL connection successful (SELECT 1 returned successfully).")


if __name__ == "__main__":
    try:
        check_environment()
    except Exception as error:
        print(f"PostgreSQL connection failed: {error}")
        raise SystemExit(1) from error