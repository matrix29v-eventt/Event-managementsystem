import pytest
from tests.test_utils import get_admin_headers, get_client_headers, get_unauthorized_headers

# NOTE: Venue ID 1 and Vendor ID 1 are created in conftest.py
VENUE_DATA = {
    "name": "New Venue",
    "location": "Central Hub",
    "capacity": 1000
}
VENDOR_DATA = {
    "name": "New Vendor",
    "service_type": "Security",
    "contact": "new@vendor.com"
}

# ==================================
# VENUE TESTS (Admin Only for POST)
# ==================================

def test_1_admin_can_create_venue(client):
    headers = get_admin_headers(client)
    response = client.post("/venues/", json=VENUE_DATA, headers=headers)
    assert response.status_code == 201
    assert response.json()["name"] == "New Venue"

def test_2_client_cannot_create_venue(client):
    headers = get_client_headers(client)
    response = client.post("/venues/", json=VENUE_DATA, headers=headers)
    assert response.status_code == 403 

def test_3_authenticated_can_read_venues(client):
    # This endpoint is protected by get_current_client
    headers = get_client_headers(client)
    response = client.get("/venues/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1 # Checks for the venue created in conftest.py (ID 1)

# ==================================
# VENDOR TESTS (Admin Only for POST)
# ==================================

def test_4_admin_can_create_vendor(client):
    headers = get_admin_headers(client)
    response = client.post("/vendors/", json=VENDOR_DATA, headers=headers)
    assert response.status_code == 201
    assert response.json()["service_type"] == "Security"

def test_5_client_cannot_create_vendor(client):
    headers = get_client_headers(client)
    response = client.post("/vendors/", json=VENDOR_DATA, headers=headers)
    assert response.status_code == 403 
    
def test_6_authenticated_can_read_vendors(client):
    # This endpoint is protected by get_current_client
    headers = get_admin_headers(client)
    response = client.get("/vendors/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1 # Checks for the vendor created in conftest.py (ID 1)