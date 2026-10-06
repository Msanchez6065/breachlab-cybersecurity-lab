"""Flask entry point used by Docker and local development."""

from app import create_app

app = create_app()