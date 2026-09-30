# tests/test_health.py — SRE liveness/readiness contract tests.
def test_health_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready_returns_connected(client):
    response = client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["database"] == "connected"


def test_root_still_running(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
