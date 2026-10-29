# BreachLab

BreachLab is a small educational cybersecurity project for learning how to build, inspect, test, fix, and retest software in a controlled local environment.

## Why I Am Building It

This project provides a simple place to learn software engineering and cybersecurity concepts incrementally. Version 0.1 is a foundation, not a penetration-testing platform, and does not contain intentional vulnerabilities.

## Current Version

**0.1**

## Architecture

```text
Browser
  ↓
Flask Web Application
  ↓
PostgreSQL Database
```

Flask serves the home page, a non-functional login demonstration interface, and a health endpoint. PostgreSQL stores the basic User model.

## Technologies

- Python 3.12
- Flask
- Flask-SQLAlchemy and SQLAlchemy
- PostgreSQL with the Psycopg driver
- Docker and Docker Compose
- HTML and CSS
- pytest

## Current Functionality

- Home page titled “BreachLab Security Testing Environment”
- `/health` endpoint that reports Flask and database connectivity
- User model with `id`, `username`, `password_hash`, and `role`
- Idempotent seed script for fake employee, manager, and administrator users; generated passwords are random and only hashes are stored
- Login page interface only; authentication is not implemented
- Environment check script and a basic health test

## Run With Docker

Prerequisites: install and start Docker Desktop with Docker Compose available.

From the project directory, create your local environment file:

```powershell
Copy-Item .env.example .env
```

The example password is for local-only development. Replace it in `.env` with a value of your choice before using the project. `.env` is ignored by Git.

Build and start the Flask and PostgreSQL services:

```powershell
docker compose up --build -d
```

Initialize the User table and add fake test users:

```powershell
docker compose exec web python -m scripts.seed_database
```

Verify the app container can query PostgreSQL:

```powershell
docker compose exec web python -m scripts.check_environment
```

Expected output:

```text
PostgreSQL connection successful (SELECT 1 returned successfully).
```

Open **http://localhost:5000** for the home page. Open **http://localhost:5000/health** for JSON similar to:

```json
{"database":"connected","status":"running"}
```

To stop the services, run `docker compose down`. To also delete the local database volume and its data, run `docker compose down -v`.

## Tests

With the dependencies installed, run `python -m pytest`. The health test uses an in-memory SQLite database, so pytest does not require Docker or PostgreSQL. The separate environment check verifies PostgreSQL connectivity.

## Planned Cybersecurity Features

Potential future exercises are listed in [docs/future-vulnerabilities.md](docs/future-vulnerabilities.md). They are planned scenarios only and have not been implemented. Future versions may build a controlled testing workflow that records findings, remediation, and retests.
[Visit](https://chatgpt.com)

## Disclaimer

BreachLab is an educational cybersecurity project designed for testing within isolated environments. It is not intended for unauthorized testing of systems or networks. Keep future vulnerable exercises local and isolated, and only test systems for which you have explicit authorization.
