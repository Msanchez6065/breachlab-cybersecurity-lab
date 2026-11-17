# BreachLab Progress

## Status Key

| Status | Meaning |
|---|---|
| **Planned** | Agreed on, no code yet |
| **In progress** | Partially built |
| **Implemented** | Code or configuration exists but has not been run and confirmed |
| **Verified (manual)** | Run by hand and the result confirmed |
| **Verified (automated)** | Covered by a passing pytest test |
| **Not verified** | Not yet run or tested |

---

## Milestone 0 — Understand and Verify the Existing Foundation

**Status:** Complete (2026-11-17)
**Last verified:** 2026-11-13
**Environment:** Windows host · Docker Desktop 4.48.0 (Engine 28.5.1) · Docker Compose v2.40.0 · container Python 3.12.16 · pytest 8.4.2
**Verified at commit:** `290e06a` (code unchanged since; only README edited afterward)

### Verification Results

| Item | Status | Evidence / Notes |
|---|---|---|
| Local repository matches GitHub | Verified (manual) | Fetched, reviewed diff, fast-forwarded to `290e06a` |
| Compose configuration and `.env` | Verified (manual) | `docker compose config --quiet` returned no errors |
| Web image builds | Verified (manual) | `docker compose build` completed successfully |
| Containers start; db healthy | Verified (manual) | `docker compose ps`: both up, db `(healthy)` |
| Healthcheck-based startup ordering (configuration) | Verified (manual) | `docker-compose.yml` defines a `pg_isready` healthcheck and `depends_on: condition: service_healthy`; Compose accepted the configuration |
| Healthcheck-based startup ordering (behavior) | Partially verified | Normal startup was consistent with the gate: both containers created 38s earlier, web up 32s. Behavior when the database is unhealthy has **not** been tested |
| PostgreSQL not published to the host | Verified (manual) | db shows `5432/tcp` with no host mapping |
| Seed script creates fake users | Verified (manual) | First run: "Added 3 fake test user(s)" on a fresh volume |
| Seed script is idempotent | Verified (manual) | Second run: "Added 0 fake test user(s)" |
| App-to-PostgreSQL connectivity | Verified (manual) | `scripts.check_environment` reported success |
| `/health` returns 200 + JSON | Verified (manual) + Verified (automated) | `curl.exe -i` returned 200 and expected JSON; pytest test passes (against SQLite) |
| `/health` returns 503 when DB is down | Implemented | Code path exists; not tested manually or automatically |
| Home page and CSS render | Verified (manual) | Viewed in browser; styles applied |
| Login page renders | Verified (manual) | Form displayed in browser |
| Login authentication | Implemented (interface only) | POST shows "not implemented" message; route checks only the request method and never reads `request.form` or queries the database |
| Test suite runs in container | Verified (manual) | `docker compose exec web python -m pytest -v`: 1 passed |
| Tests run from the Windows host | Not verified | Not attempted; host Python dependencies not installed |

### Test Coverage Notes

- One automated test exists (`tests/test_basic.py`). It checks `/health` using an **in-memory SQLite** database, not PostgreSQL.
- Not covered by automated tests: PostgreSQL connectivity, the 503 path, home and login pages, the User model, and the seed script.
- Plain `pytest` fails to import the `app` package; use `python -m pytest`.

### Milestone 0 Remaining Work

- [x] Verify the existing setup end to end
- [x] Remove stray external link from README (`b275e18`)
- [x] Update this progress tracker
- [ ] Align résumé description with actual functionality (deferred by choice)
- [x] Explain each project file (docker-compose.yml explained back; remaining files reviewed via notes)
- [x] Write the Milestone 0 journal entry (docs/journal/m0.md)

---

## Milestone 1 — Lab Networking and Isolation

**Status:** Complete (2026-11-17)
**Branch:** `m1-network-isolation`

### Changes

- Web port published on localhost only: `127.0.0.1:5000:5000` (remediates OBS-01)
- Two Docker networks: `frontend` (web, attacker) and `backend` (web, db), with `backend` marked `internal: true`
- New `attacker` service (`attacker/Dockerfile`): Python 3.12 slim image with nmap, curl, ping, and dnsutils, attached to `frontend` only

### Verification Results

| Item | Status | Evidence / Notes |
|---|---|---|
| Web published on localhost only | Verified (manual) | `docker compose ps`: only `127.0.0.1:5000->5000/tcp` |
| App reachable from the host | Verified (manual) | `curl.exe -i http://localhost:5000/health`: 200 |
| Web reaches PostgreSQL over `backend` | Verified (manual) | `/health` reports `"database":"connected"` |
| Data persists across `down` / `up` | Verified (manual) | Seed reported "Added 0" after containers and networks were recreated |
| `backend` membership | Verified (manual) | `docker network inspect`: web, db |
| `frontend` membership | Verified (manual) | `docker network inspect`: web only (checked before the attacker was added) |
| Attacker reaches web by name | Verified (manual) | From attacker: `curl -i http://web:5000/health` returned 200 |
| Attacker cannot resolve `db` | Verified (manual) | From attacker: `nslookup db` returned SERVFAIL |
| Attacker cannot reach PostgreSQL by IP | Verified (manual) | From attacker: `nmap -Pn -p 5432 172.19.0.2` reported `filtered` |
| Scanner control test | Verified (manual) | From attacker: `nmap -Pn -p 5000 web` reported `open`, confirming the `filtered` result is meaningful |
| `db` has no internet access | Verified (manual) | From db: `ping -c 2 -W 2 8.8.8.8` returned "Network unreachable" |
| Attacker internet access | Not verified | Expected, since `frontend` is not internal; not tested |
| Automated segmentation tests | Planned | To be added with the M3 CLI |

### Notes

- `docker compose down` only removes networks defined in the current file. The orphaned v0.1 `default` network was removed manually.
- With `-Pn`, nmap's "Host is up" reflects the flag's assumption, not confirmed reachability.
- nmap labels port 5000 as `upnp` based on the port number alone; the service is actually Flask.

---

## Security Observations

These are observations about the lab infrastructure, not intentionally planted vulnerabilities. Severity reflects **current** risk.

| ID | Observation | Severity | Status | Planned Fix |
|---|---|---|---|---|
| OBS-01 | Web port published on all host interfaces (`0.0.0.0:5000` and `[::]:5000`) | Low | Remediated (retested 2026-11-17) | Fixed in M1: bound to `127.0.0.1:5000:5000` |
| OBS-02 | `Server` header discloses `Werkzeug/3.1.9 Python/3.12.16` | Informational | Verified (manual) | Later milestone: explicitly control the `Server` header and re-verify |

### OBS-01 — Web Service Exposed on All Network Interfaces

- **Evidence:** `docker compose ps` shows `0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp`.
- **Why it matters:** The app accepts connections on every network interface of the host, not just localhost. Whether other devices on the same network can actually reach it depends on the Windows firewall, which has not been tested.
- **Severity: Low.** The app currently has no working authentication, no sensitive functionality, and only fake data, so an attacker on the local network would gain very little.
- **Risk note:** This risk would increase significantly once intentional vulnerabilities are introduced, because anyone able to reach port 5000 could exploit them. For that reason, remediation is scheduled for M1, **before** any vulnerabilities are added. The severity will be reassessed if the issue is still present at that point.
- **Remediation:** Publish the port as `127.0.0.1:5000:5000`, then confirm with `docker compose ps` that only `127.0.0.1` is listed.
- **Retest (2026-11-17):** `docker compose ps` shows only `127.0.0.1:5000->5000/tcp`; the `0.0.0.0` and `[::]` bindings are gone, and the app remains reachable from the host. **Status: Remediated.**

### OBS-02 — Server Version Disclosure

- **Evidence:** `curl.exe -i http://localhost:5000/health` returned `Server: Werkzeug/3.1.9 Python/3.12.16`.
- **Why it matters:** It reveals the framework, the exact versions, and that Flask's development server is in use. That speeds up an attacker's reconnaissance (fingerprinting and looking up known vulnerabilities).
- **Severity: Informational.** It is not directly exploitable and grants no access by itself. It would be reassessed if a disclosed version had a known, relevant vulnerability.
- **Remediation:** Replace the development server with a production-grade setup and **explicitly control the `Server` header** (for example, at a reverse proxy). Changing servers alone is not assumed to fix this, since production servers may send their own identifying header. Re-run `curl.exe -i` afterward to confirm what is actually disclosed.

---

## Upcoming Milestones

| Milestone | Description | Status |
|---|---|---|
| M1 | Lab networking and isolation (attacker container, two networks, localhost binding) | Complete (2026-11-17) |
| M2 | Functional authentication and authorization | Planned |
| M3 | Python CLI, reconnaissance, and enumeration (with scope enforcement) | Planned |
| M4 | Information exposure and weak authentication | Planned |
| M5 | SQL injection and IDOR | Planned |
| M6 | Findings management and HTML reporting | Planned |
| M7 | Full penetration test, remediation, and retesting | Planned |
| M8 | GitHub portfolio and résumé preparation | Planned |

Automated tests will be added within each milestone, including vulnerable-behavior and secure-behavior tests for every intentional vulnerability.