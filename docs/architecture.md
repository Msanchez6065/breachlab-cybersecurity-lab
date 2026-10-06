# BreachLab Architecture

## Version 0.1

```text
Browser
  ↓
Flask Web Application
  ↓
PostgreSQL Database
```

The browser requests the home page, login demonstration interface, or health endpoint from Flask. Flask uses PostgreSQL for the User model. The `/health` endpoint checks database connectivity with a simple `SELECT 1` query.

## Possible Future Testing Flow

```text
Attacker/Test Machine
  ↓
Reconnaissance / Security Testing
  ↓
BreachLab Application
  ↓
Finding
  ↓
Remediation
  ↓
Retest
```

This is a possible future learning workflow, not a capability implemented in Version 0.1. Any future exercises must remain inside an isolated BreachLab environment.