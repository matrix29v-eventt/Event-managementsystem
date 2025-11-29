from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 💡 NEW: Import CORS Middleware
from app.db import engine, Base
from app.models import models
from app.routers import clients, venues, vendors, events, bookings, payments, auth # Ensure 'auth' is imported

# Create database tables (NOTE: This is typically replaced by Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System")

# --- CORS Configuration (FIXES THE 405/OPTIONS ERROR) ---
origins = [
    "http://localhost:3000",      # Allow the React development server
    "http://127.0.0.1:3000",      # Allow 127.0.0.1 as a safe alternative
    # Add your final production domain here when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # List of allowed origins
    allow_credentials=True,        # Allow cookies/authorization headers
    allow_methods=["*"],           # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],           # Allow all headers (especially Authorization)
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