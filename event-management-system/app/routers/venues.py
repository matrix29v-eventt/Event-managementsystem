# app/routers/venues.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required

router = APIRouter(
    prefix="/venues",
    tags=["Venues"]
)

# POLICY: Admin Only (Creation)
@router.post("/", response_model=schemas.Venue, status_code=status.HTTP_201_CREATED)
def create_venue(
    venue: schemas.VenueCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin")) # Requires admin role
):
    return crud.create_venue(db=db, venue=venue)

# POLICY: Authenticated (Read All)
@router.get("/", response_model=List[schemas.Venue])
def read_venues(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_client) # Requires any valid token
):
    venues = crud.get_venues(db, skip=skip, limit=limit)
    return venues

# POLICY: Authenticated (Read Single)
@router.get("/{venue_id}", response_model=schemas.Venue)
def read_venue(
    venue_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_client) # Requires any valid token
):
    db_venue = crud.get_venue(db, venue_id=venue_id)
    if db_venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return db_venue

# Add PUT/DELETE endpoints here and protect them with role_required("admin")