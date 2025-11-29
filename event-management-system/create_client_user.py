import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for imports
sys.path.append(str(Path(__file__).resolve().parents[0])) 
load_dotenv() 

from app.db import SessionLocal
from app.crud.crud import create_client, get_client_by_email
from app.schemas.schemas import ClientCreate

# --- Client Credentials ---
CLIENT_EMAIL = "client@ems.com"
CLIENT_PASS = "testpassword123"

def create_standard_client():
    db = SessionLocal()
    try:
        # Check if client already exists
        if get_client_by_email(db, email=CLIENT_EMAIL):
            print(f"User {CLIENT_EMAIL} already exists. Skipping creation.")
            return

        # Create the Pydantic model
        client_data = ClientCreate(
            name="Standard Client",
            email=CLIENT_EMAIL,
            phone="0987654321",
            password=CLIENT_PASS
        )
        
        # Call the secure CRUD function, defaulting the role to "client"
        new_client = create_client(db=db, client=client_data, role="client")
        print(f"\n✅ Standard Client Created Successfully:")
        print(f"   Email: {new_client.email}")
        print(f"   Role: {new_client.role}")

    except Exception as e:
        print(f"\n❌ ERROR during client creation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_standard_client()