import pytest
from datetime import date, timedelta
from tests.test_utils import get_admin_headers, get_client_headers, get_unauthorized_headers

# Constants used for verification
CLIENT_ID = 2  # Standard Client ID
VENUE_ID = 1   # Venue ID created in conftest.py

VALID_EVENT_DATA = {
    "name": "Birthday Bash",
    "date": (date.today() + timedelta(days=30)).isoformat(),
    "client_id": CLIENT_ID,
    "venue_id": VENUE_ID
}

# ==================================
# EVENT TESTS (Client Only for POST)
# ==================================

def test_1_client_can_create_own_event(client):
    headers = get_client_headers(client)
    # This test should now pass after removing 'description' from crud.create_event
    response = client.post("/events/", json=VALID_EVENT_DATA, headers=headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Birthday Bash"

def test_2_client_cannot_create_event_for_admin(client):
    headers = get_client_headers(client)
    bad_data = VALID_EVENT_DATA.copy()
    bad_data["client_id"] = 1 # Admin ID
    response = client.post("/events/", json=bad_data, headers=headers)
    assert response.status_code == 403

def test_3_admin_cannot_create_event(client):
    headers = get_admin_headers(client)
    response = client.post("/events/", json=VALID_EVENT_DATA, headers=headers)
    assert response.status_code == 403

def test_4_client_can_read_own_event(client):
    headers = get_client_headers(client)
    EVENT_ID = 1 # Event created in test 1
    # This test should now pass because the event was created in test 1
    response = client.get(f"/events/{EVENT_ID}", headers=headers)
    assert response.status_code == 200
    assert response.json()["client_id"] == CLIENT_ID

def test_5_unauthorized_cannot_read_event(client):
    headers = get_unauthorized_headers()
    EVENT_ID = 1
    response = client.get(f"/events/{EVENT_ID}", headers=headers)
    assert response.status_code == 401