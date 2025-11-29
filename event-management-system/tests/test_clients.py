import pytest
from app.schemas.schemas import ClientCreate
from tests.test_utils import get_admin_headers, get_client_headers, get_unauthorized_headers

# Global Test Data (for login and registration tests)
TEST_PASSWORD = "testpassword123"
TEST_ADMIN = {
    "name": "Admin User", "email": "admin@ems.com", "phone": "1234567890", "password": TEST_PASSWORD
}
TEST_CLIENT = {
    "name": "Standard Client", "email": "client@ems.com", "phone": "0987654321", "password": TEST_PASSWORD
}


# 1. Test Client Registration (Testing for duplicate failure only)
def test_create_client(client): 
    # The Admin and Client are ALREADY created by the conftest fixture.
    
    # Test duplicate email to ensure validation works
    response_duplicate = client.post("/clients/", json=TEST_CLIENT)
    assert response_duplicate.status_code == 400


# 2. Test Secured Endpoint (GET All Clients - Admin Only)
def test_get_clients_admin_only(client):
    admin_token = get_admin_headers(client)["Authorization"]
    client_token = get_client_headers(client)["Authorization"]
    
    # SUCCESS: Admin accessing all clients (ID 1 is admin)
    admin_headers = {"Authorization": admin_token}
    response_admin = client.get("/clients/", headers=admin_headers)
    assert response_admin.status_code == 200
    assert len(response_admin.json()) >= 2
    
    # FAILURE: Standard Client accessing Admin-only route (Forbidden)
    client_headers = {"Authorization": client_token}
    response_client = client.get("/clients/", headers=client_headers)
    assert response_client.status_code == 403


# 3. Test Authorization Check (GET Self Profile)
def test_get_client_self_access(client):
    client_headers = get_client_headers(client)
    
    CLIENT_ID = 2
    ADMIN_ID = 1
    
    # SUCCESS: Client accessing their OWN profile (ID 2)
    response_self = client.get(f"/clients/{CLIENT_ID}", headers=client_headers)
    assert response_self.status_code == 200
    assert response_self.json()["email"] == TEST_CLIENT["email"]
    
    # FAILURE: Client trying to access Admin's profile (ID 1)
    response_other = client.get(f"/clients/{ADMIN_ID}", headers=client_headers)
    assert response_other.status_code == 403 # Not authorized

# 4. Test Invalid Token
def test_get_clients_invalid_token(client):
    invalid_headers = {"Authorization": "Bearer invalid_jwt_token"}
    response = client.get("/clients/", headers=invalid_headers)
    assert response.status_code == 401 # Unauthorized (JWTError)