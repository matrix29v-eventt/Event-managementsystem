# tests/test_api.py — representative API + invalid-input + DB-behaviour tests.
from tests.test_utils import get_admin_headers, get_client_headers


def test_list_venues_as_client(client):
    """Representative read path: authenticated client can list venues (seeded row exists)."""
    headers = get_client_headers(client)
    response = client.get("/venues/", headers=headers)
    assert response.status_code == 200
    venues = response.json()
    assert isinstance(venues, list)
    assert len(venues) >= 1


def test_admin_can_create_venue(client):
    headers = get_admin_headers(client)
    response = client.post(
        "/venues/",
        json={"name": "SRE Test Hall", "location": "Pipeline City", "capacity": 250},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "SRE Test Hall"


def test_read_single_venue(client):
    headers = get_client_headers(client)
    response = client.get("/venues/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Setup Venue"


def test_read_missing_venue_returns_404(client):
    """Error-handling contract: unknown IDs return 404 with a detail message."""
    headers = get_client_headers(client)
    response = client.get("/venues/999999", headers=headers)
    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_venue_invalid_input_returns_422(client):
    """Invalid-input contract: Pydantic validation failures surface as 422, never 500."""
    headers = get_admin_headers(client)
    response = client.post(
        "/venues/",
        json={"name": "Bad Venue", "location": "Nowhere"},  # missing required capacity
        headers=headers,
    )
    assert response.status_code == 422


def test_create_venue_wrong_type_returns_422(client):
    headers = get_admin_headers(client)
    response = client.post(
        "/venues/",
        json={"name": "Bad Venue", "location": "Nowhere", "capacity": "huge"},
        headers=headers,
    )
    assert response.status_code == 422


def test_created_venue_persisted_in_db(client):
    """DB-behaviour contract: a created row is readable back (write → read round-trip)."""
    admin_headers = get_admin_headers(client)
    created = client.post(
        "/venues/",
        json={"name": "Persisted Hall", "location": "DB City", "capacity": 50},
        headers=admin_headers,
    )
    assert created.status_code == 201
    venue_id = created.json()["id"]

    fetched = client.get(f"/venues/{venue_id}", headers=get_client_headers(client))
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Persisted Hall"
