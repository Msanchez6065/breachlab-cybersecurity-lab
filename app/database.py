"""Database extension and environment-based PostgreSQL configuration."""

import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL

db = SQLAlchemy()


def get_database_url():
    """Build a PostgreSQL URL from environment variables without hardcoded secrets."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("POSTGRES_DB"),
    )