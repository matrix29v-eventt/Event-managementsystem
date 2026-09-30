# tests/test_auth.py — SRE authentication contract tests.
from tests.test_utils import TEST_ADMIN, TEST_CLIENT, get_admin_headers


def test_login_admin_success(client):
    response = client.post("/auth/token", json=TEST_ADMIN)
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert "client_id" in body


def test_login_client_success(client):
    response = client.post("/auth/token", json=TEST_CLIENT)
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_wrong_password_rejected(client):
    response = client.post(
        "/auth/token", json={"email": TEST_ADMIN["email"], "password": "wrong-password"}
    )
    assert response.status_code == 401


def test_login_unknown_user_rejected(client):
    response = client.post(
        "/auth/token", json={"email": "nobody@example.com", "password": "whatever123"}
    )
    assert response.status_code == 401


def test_protected_route_without_token_rejected(client):
    response = client.get("/venues/")
    assert response.status_code == 401


def test_protected_route_with_bad_token_rejected(client):
    response = client.get("/venues/", headers={"Authorization": "Bearer invalid.token.xyz"})
    assert response.status_code == 401


def test_client_cannot_perform_admin_action(client):
    # Venue creation is admin-only; a valid client token must get 403 (not 401/201).
    from tests.test_utils import get_client_headers

    headers = get_client_headers(client)
    response = client.post(
        "/venues/",
        json={"name": "Forbidden Venue", "location": "Nowhere", "capacity": 10},
        headers=headers,
    )
    assert response.status_code == 403


def test_admin_token_accepted_on_protected_route(client):
    headers = get_admin_headers(client)
    response = client.get("/venues/", headers=headers)
    assert response.status_code == 200
