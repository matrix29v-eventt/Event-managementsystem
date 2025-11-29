import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path for imports
# This line is crucial for finding 'app.db' and 'app.crud.crud'
sys.path.append(str(Path(__file__).resolve().parents[0])) 
load_dotenv() 

from app.db import SessionLocal
from app.crud.crud import create_client
from app.schemas.schemas import ClientCreate
from app.crud.crud import get_client_by_email

# --- Admin Credentials (Must match test data for consistency) ---
ADMIN_EMAIL = "admin@ems.com"
ADMIN_PASS = "testpassword123"

def create_initial_admin():
    db = SessionLocal()
    try:
        # Check if user already exists to prevent duplicates
        if get_client_by_email(db, email=ADMIN_EMAIL):
            print(f"User {ADMIN_EMAIL} already exists. Skipping creation.")
            return

        # Create the Pydantic model for the new admin
        admin_data = ClientCreate(
            name="Live Admin",
            email=ADMIN_EMAIL,
            phone="1112223333",
            password=ADMIN_PASS
        )
        
        # Call the secure CRUD function, explicitly setting the role to "admin"
        new_admin = create_client(db=db, client=admin_data, role="admin")
        print(f"\n✅ Admin User Created Successfully:")
        print(f"   Email: {new_admin.email}")
        print(f"   Role: {new_admin.role}")

    except Exception as e:
        print(f"\n❌ ERROR during admin creation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()