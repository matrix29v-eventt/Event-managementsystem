import os
import logging
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import engine, Base, get_db
from app.models import models  # noqa: F401 - registers models for create_all
from app.routers import (
    clients,
    venues,
    vendors,
    events,
    bookings,
    payments,
    auth,
)  # Ensure 'auth' is imported


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup, but don't crash if DB is unavailable (e.g. during import/tests)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.warning(f"Could not create DB tables on startup: {e}")
    yield


app = FastAPI(title="Event Management System", lifespan=lifespan)

# Consistent, greppable application logs (used by scripts/logs.sh and CI smoke tests).
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("ems")

# --- CORS Configuration (FIXES THE 405/OPTIONS ERROR) ---
origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies/authorization headers
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers (especially Authorization)
)
# --------------------------------------------------------

# Include routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(venues.router)
app.include_router(vendors.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(payments.router)


@app.get("/")
def root():
    return {"message": "Event Management System API running"}


@app.get("/health", tags=["Operations"])
def health():
    """Liveness probe: confirms the application process is running.

    Deliberately dependency-free (no DB) so orchestrators and load
    balancers can distinguish 'process alive' from 'ready to serve'.
    """
    return {"status": "healthy"}


@app.get("/ready", tags=["Operations"])
def ready(db: Session = Depends(get_db)):
    """Readiness probe: confirms the app can serve traffic, including DB connectivity.

    Uses the request-scoped ``get_db`` session (rather than the raw engine) so the
    check reflects exactly what a real request would experience — and so the test
    suite's ``get_db`` override exercises the same code path.
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - surfaced as JSON for operators
        logger.warning("readiness check failed: %s", exc)
        return {"status": "not_ready", "database": "disconnected"}
    return {"status": "ready", "database": "connected"}
