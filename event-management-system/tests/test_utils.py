# tests/test_utils.py
from typing import Dict
from starlette.testclient import TestClient # Used for type hinting

# Global Test Data (Should match the data used in conftest.py)
TEST_PASSWORD = "testpassword123"
TEST_ADMIN = {
    "email": "admin@ems.com", "password": TEST_PASSWORD
}
TEST_CLIENT = {
    "email": "client@ems.com", "password": TEST_PASSWORD
}

def get_token(client: TestClient, user_data: Dict) -> str:
    """Helper function to log in a user and return the JWT token."""
    response = client.post(
        "/auth/token",
        json=user_data
    )
    assert response.status_code == 200
    return response.json()["access_token"]

def get_admin_headers(client: TestClient) -> Dict[str, str]:
    """Returns headers for the Admin user."""
    token = get_token(client, TEST_ADMIN)
    return {"Authorization": f"Bearer {token}"}

def get_client_headers(client: TestClient) -> Dict[str, str]:
    """Returns headers for the Standard Client user."""
    token = get_token(client, TEST_CLIENT)
    return {"Authorization": f"Bearer {token}"}

def get_unauthorized_headers() -> Dict[str, str]:
    """Returns invalid headers for unauthorized tests."""
    return {"Authorization": "Bearer invalid.token.xyz"}