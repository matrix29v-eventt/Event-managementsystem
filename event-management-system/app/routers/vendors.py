# app/routers/vendors.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)

# POLICY: Admin Only (Creation)
@router.post("/", response_model=schemas.Vendor, status_code=status.HTTP_201_CREATED)
def create_vendor(
    vendor: schemas.VendorCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin")) # Requires admin role
):
    return crud.create_vendor(db=db, vendor=vendor)

# POLICY: Authenticated (Read All)
@router.get("/", response_model=List[schemas.Vendor])
def read_vendors(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_client) # Requires any valid token
):
    vendors = crud.get_vendors(db, skip=skip, limit=limit)
    return vendors

# POLICY: Authenticated (Read Single)
@router.get("/{vendor_id}", response_model=schemas.Vendor)
def read_vendor(
    vendor_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_client) # Requires any valid token
):
    db_vendor = crud.get_vendor(db, vendor_id=vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

# Add PUT/DELETE endpoints here and protect them with role_required("admin")