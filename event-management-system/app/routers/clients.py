# app/routers/clients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.models.models import Client # For type hinting the current user
from app.auth import get_current_client, role_required

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

# POLICY: Public/Open Registration
@router.post("/", response_model=schemas.Client, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_client(db=db, client=client)

# POLICY: Admin Only
@router.get("/", response_model=List[schemas.Client])
def read_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Client = Depends(role_required("admin")) # Requires admin role
):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

# POLICY: Self or Admin Only
@router.get("/{client_id}", response_model=schemas.Client)
def read_client(
    client_id: int, 
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client) # Requires any valid token
):
    # Authorization Check: Client can only view their own profile unless they are an Admin
    if current_user.id != client_id and current_user.role != "admin":
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this client")
         
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Add PUT/DELETE endpoints with similar authorization logic