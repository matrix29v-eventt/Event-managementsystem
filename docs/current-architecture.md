# Current Architecture — Secure Event Management System

> Inspection date: 2026-09-30. No application logic was changed to produce this document.

## 1. Repository layout (monorepo)

```text
Event-managementsystem/
├── docker-compose.yml                # Root orchestration: postgres_db + backend + frontend
├── .env                              # Local secrets (git-ignored, present locally)
├── .gitignore                        # Root ignore rules
├── README.md                         # Short overview (full Docker instructions)
├── event-management-system/          # FastAPI backend (SRE scope of this project)
│   ├── app/
│   │   ├── main.py                   # FastAPI entry point (`app.main:app`)
│   │   ├── db.py                     # SQLAlchemy engine + SessionLocal + get_db
│   │   ├── auth.py                   # JWT creation / verification, RBAC helpers
│   │   ├── models/models.py          # Client, Venue, Vendor, Event, Booking, Payment
│   │   ├── schemas/schemas.py        # Pydantic v2 request/response models
│   │   ├── crud/crud.py              # DB access layer + password hashing
│   │   ├── routers/                  # auth, clients, venues, vendors, events, bookings, payments
│   │   └── notifications.py          # Optional SendGrid email notifications
│   ├── alembic/ + alembic.ini        # Migrations (URL injected from DATABASE_URL via env.py)
│   ├── tests/                        # Pytest suite (conftest.py + 5 test modules)
│   ├── requirements.txt              # Pinned pip dependencies (Python 3.11)
│   ├── Dockerfile                    # Single-stage python:3.11-slim image
│   ├── .dockerignore                 # Excludes pycache, .env, venv, tests artefacts
│   ├── create_admin.py / create_client_user.py  # Manual seed helpers
│   └── test.db                       # SQLite fallback artefact (local testing only)
└── event-management-frontend/        # React UI (out of SRE scope, only composed)
```

## 2. Backend framework & entry point

- **Framework:** FastAPI 0.116.1 + Uvicorn 0.35.0, Pydantic v2, SQLAlchemy 2.0 (ORM).
- **Entry point:** `app/main.py` → `app` object, served as `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
- **Startup:** `lifespan` context manager runs `Base.metadata.create_all(bind=engine)` inside
  try/except so the app can still be imported when the DB is unreachable (tests/CI).
- **CORS:** origins from `CORS_ORIGINS` env var (default `http://localhost:3000,http://127.0.0.1:3000`).

## 3. Dependency management

- `event-management-system/requirements.txt` with pinned versions.
- Key packages: `fastapi`, `uvicorn`, `SQLAlchemy`, `psycopg2-binary`, `alembic`,
  `python-jose[cryptography]`, `passlib`, `bcrypt`, `python-multipart`, `sendgrid`,
  `pytest`, `pytest-asyncio`, `httpx`, `python-dotenv`.
- No lock file, no lint tooling (added by the SRE layer: Ruff in CI).

## 4. Database configuration

- **Engine:** created in `app/db.py` from `DATABASE_URL` (required — `ValueError` if unset).
- **Local/docker value:** `postgresql://<user>:<password>@postgres_db/<db>`
  (host `postgres_db` inside Compose network, `localhost` outside; concrete
  local defaults live in untracked `.env`, never in this doc).
- **Session:** `SessionLocal` + `get_db` generator dependency per request.
- **Migrations:** Alembic configured, URL resolved dynamically from `DATABASE_URL` in `env.py`.
  Runtime table creation also happens via `Base.metadata.create_all` on startup.
- **Tests:** `tests/conftest.py` uses `TEST_DATABASE_URL`, falling back to
  `sqlite:///./test.db` (with `check_same_thread=False`). App `get_db` is overridden
  with a `TestingSessionLocal`; schema created/dropped by session-scoped fixtures plus
  seed data (admin + client users, one venue/vendor/event/booking).

## 5. Existing Docker files

- `event-management-system/Dockerfile` (single stage): `python:3.11-slim`, `pip install -r
  requirements.txt`, `COPY . .`, `EXPOSE 8000`, `CMD uvicorn app.main:app ...`.
  Gaps fixed by SRE layer: runs as root, no dependency-layer caching optimisation,
  no `curl`/health probe, dev `--reload` flag comes from Compose command.
- `event-management-system/.dockerignore`: covers `__pycache__`, `*.pyc`, `.env`,
  venvs, `.git`, tests artefacts. (A root-level `.dockerignore` did not exist.)
- Root `docker-compose.yml`: three services —
  - `postgres_db` (`postgres:14-alpine`, named volume `postgres_data`, `pg_isready` healthcheck,
    credentials from `POSTGRES_*` with defaults),
  - `backend` (builds `./event-management-system`, `env_file: .env`, waits on
    `service_healthy` postgres, maps `8000:8000`, overrides `DATABASE_URL`/`CORS_ORIGINS`,
    runs uvicorn with `--reload`),
  - `frontend` (builds `./event-management-frontend`, maps `3000:80`).
- No staging/prod Compose files, no restart policies, no API healthcheck — all added later.

## 6. Existing tests

| File | Covers |
|---|---|
| `tests/conftest.py` | Engine/session override, schema setup, seed data, `TestClient` fixture |
| `tests/test_utils.py` | Login helpers (`get_admin_headers`, `get_client_headers`, …) |
| `tests/test_clients.py`, `test_events.py`, `test_venues_vendors.py`, `test_bookings_payments.py` | RBAC + CRUD per domain |

Run with a single command (`pytest`) from `event-management-system/`.
Gaps: no health/readiness tests, no invalid-input test file, no standalone auth test —
added as `test_health.py`, `test_auth.py`, `test_api.py`.

## 7. Environment variables

From root `.env` (all secrets local-only, never committed as real values in `.env.example`):

| Variable | Purpose |
|---|---|
| `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT signing/verification (`app/auth.py`) |
| `POSTGRES_USER/PASSWORD/DB` | Postgres container credentials |
| `DATABASE_URL` / `TEST_DATABASE_URL` | Runtime / test SQLAlchemy URLs |
| `CORS_ORIGINS`, `REACT_APP_API_URL` | Browser + frontend build config |
| `SENDGRID_API_KEY`, `NOTIFICATION_FROM_EMAIL` | Optional email (empty = disabled) |

## 8. Authentication mechanism

- `POST /auth/token` accepts `{email, password}` JSON (`app/schemas/schemas.py::Login`),
  verifies bcrypt hash via `passlib`, returns `{"access_token", "token_type": "bearer", "client_id"}`.
- Token payload: `sub=email`, `role`, `client_id`, `exp` timestamp; HS256 via `python-jose`.
- Per-request: `OAuth2PasswordBearer(tokenUrl="auth/token")` → `get_current_client`
  (401 on bad token/unknown user) → `role_required("admin")` (403 on wrong role).
- RBAC policy examples: anyone authenticated can list venues; only `admin` can create them;
  clients can only create events for their own `client_id`.

## 9. API routes

| Router | Prefix | Notes |
|---|---|---|
| auth | `/auth` | `POST /auth/token` (login) |
| clients | `/clients` | Registration + admin-only user management |
| venues | `/venues` | CRUD; create/update/delete admin-only |
| vendors | `/vendors` | Same policy shape as venues |
| events | `/events` | Clients create own events; admins on behalf of anyone |
| bookings | `/bookings` | Links events ↔ vendors with `service_cost` |
| payments | `/payments` | Records against bookings |
| root | `/` | `GET /` → `{"message": "Event Management System API running"}` |

No `/health` or `/ready` endpoints existed — added by Phase 3.

## 10. Existing deployment configuration

- Local Docker Compose only (dev flags: `--reload`, no restart policy, no registry,
  no CI/CD workflows, no `.github/` directory, single `main` branch).
- Frontend served through the same Compose file; backend is the SRE focus.

## 11. Frontend (for completeness)

React app in `event-management-frontend/` (own Dockerfile, built with
`REACT_APP_API_URL` build arg, served on port 80 → mapped to 3000).
Not modified by the SRE work except being left untouched in the base Compose file;
staging/prod-like stacks deploy backend + database only to keep the SRE scope on the API.
