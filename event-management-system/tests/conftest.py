import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 💡 CRITICAL FIX: Add date imports for setup data
from datetime import date, timedelta 

# Import your application modules
from app.db import Base, get_db
from app.main import app
from app.models.models import Client, Venue, Vendor, Event, Booking, Payment 
from app.crud.crud import hash_password 
from app.schemas.schemas import ClientCreate

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ======================================================
# GLOBAL TEST DATA (Must match test_utils.py data)
# ======================================================
TEST_PASSWORD = "testpassword123"
TEST_ADMIN_DATA = {
    "name": "Admin User", "email": "admin@ems.com", "phone": "1234567890", "password": TEST_PASSWORD
}
TEST_CLIENT_DATA = {
    "name": "Standard Client", "email": "client@ems.com", "phone": "0987654321", "password": TEST_PASSWORD
}

# ------------------------------------------------------------------
# 1. TEST DATABASE SETUP
# ------------------------------------------------------------------
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") 
if not TEST_DATABASE_URL:
    raise EnvironmentError("TEST_DATABASE_URL not set in environment variables.")

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ------------------------------------------------------------------
# 2. FIXTURES
# ------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Fixture to create and drop tables for testing."""
    Base.metadata.create_all(bind=test_engine)
    yield  # Run tests
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="session")
def client():
    """Fixture to provide a synchronous TestClient."""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def create_initial_data(setup_database):
    """Creates initial users (Admin, Client) and prerequisite data (Venue, Vendor, Event, Booking)."""
    db = TestingSessionLocal()
    
    # --- 1. Create Base Users ---
    
    # Admin Client (ID 1)
    admin_schema = ClientCreate(**TEST_ADMIN_DATA)
    db_admin = Client(
        name=admin_schema.name, email=admin_schema.email, phone=admin_schema.phone,
        hashed_password=hash_password(admin_schema.password), role="admin"
    )
    db.add(db_admin)
    
    # Standard Client (ID 2)
    client_schema = ClientCreate(**TEST_CLIENT_DATA)
    db_client = Client(
        name=client_schema.name, email=client_schema.email, phone=client_schema.phone,
        hashed_password=hash_password(client_schema.password), role="client"
    )
    db.add(db_client)
    
    # --- 2. Create Prerequisite Entities ---
    
    # Venue (ID 1)
    db_venue = Venue(name="Setup Venue", location="Test Location", capacity=100)
    db_vendor = Vendor(name="Setup Vendor", service_type="Setup Service", contact="setup@vendor.com")
    
    db.add(db_venue)
    db.add(db_vendor)
    db.commit() 
    
    # --- 3. Create Event (ID 1) and Booking (ID 1)
    
    db_event_setup = Event(
        name="Setup Event",
        date=date.today() + timedelta(days=60), 
        client_id=2, # Owned by Standard Client
        venue_id=1
    )
    db.add(db_event_setup)
    db.commit() # Commit to guarantee Event ID 1 exists before Booking uses it
    
    db_booking_setup = Booking(
        event_id=1,
        vendor_id=1,
        service_cost=100.00
    )
    db.add(db_booking_setup)
    
    db.commit()
    db.close()
    yield