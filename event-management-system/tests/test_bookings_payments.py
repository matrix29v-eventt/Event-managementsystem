import pytest
from datetime import date
from tests.test_utils import get_admin_headers, get_client_headers, get_unauthorized_headers

# NOTE: Since the Booking/Payment tests rely on an Event existing, 
# we need to ensure the event test file runs first and creates event ID 1, 
# or we create the event here as a fixture. Relying on test order is fragile.
# Assuming the full suite runs, Event ID 1 exists from tests/test_events.py

EVENT_ID = 1  
VENDOR_ID = 1 

BOOKING_DATA = {
    "event_id": EVENT_ID,
    "vendor_id": VENDOR_ID,
    "service_cost": 5000.00
}

PAYMENT_DATA = {
    "event_id": EVENT_ID,
    "amount": 2500.00,
    "method": "Card", # matches schema
    "status": "Pending",
    "date": date.today().isoformat()
}

# ==================================
# BOOKING TESTS (Authenticated for POST)
# ==================================

def test_1_client_can_create_booking(client):
    # Fix: Login succeeds because client is created in conftest.py
    headers = get_client_headers(client)
    response = client.post("/bookings/", json=BOOKING_DATA, headers=headers)
    assert response.status_code == 201 

def test_2_client_cannot_read_all_bookings(client):
    headers = get_client_headers(client)
    response = client.get("/bookings/", headers=headers)
    assert response.status_code == 403 

def test_3_admin_can_read_all_bookings(client):
    headers = get_admin_headers(client)
    response = client.get("/bookings/", headers=headers)
    # Fix: Should now pass because test 1 created a booking
    assert response.status_code == 200
    assert len(response.json()) >= 1

# ==================================
# PAYMENT TESTS (Admin Only)
# ==================================

def test_4_admin_can_create_payment(client):
    headers = get_admin_headers(client)
    # Fix: Attribute Error is resolved by matching 'method' in CRUD
    response = client.post("/payments/", json=PAYMENT_DATA, headers=headers)
    assert response.status_code == 201

def test_5_client_cannot_create_payment(client):
    headers = get_client_headers(client)
    response = client.post("/payments/", json=PAYMENT_DATA, headers=headers)
    assert response.status_code == 403

def test_6_unauthorized_cannot_read_payments(client):
    headers = get_unauthorized_headers()
    response = client.get("/payments/", headers=headers)
    assert response.status_code == 401