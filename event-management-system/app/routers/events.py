# app/routers/events.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.models.models import Client
from app.auth import get_current_client, role_required

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

# POLICY: Client Only (Creation), must own the event
@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate, 
    db: Session = Depends(get_db),
    current_user: Client = Depends(role_required("client")) # Only clients can create events
):
    # Authorization Check: Ensure the event is being created for the authenticated client
    if event.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create an event for another client.")

    return crud.create_event(db=db, event=event)

# POLICY: Authenticated (Read All)
@router.get("/", response_model=List[schemas.Event])
def read_events(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client) # Requires any valid token
):
    # Optional: Filter events by current_user.id if the user is a 'client'
    if current_user.role == "client":
        # Implement a filtered CRUD function: crud.get_events_by_client(db, current_user.id)
        # For simplicity here, we assume only admins see ALL events
        pass

    events = crud.get_events(db, skip=skip, limit=limit)
    return events

# POLICY: Authenticated (Read Single)
@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    event_id: int, 
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client) # Requires any valid token
):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
        
    # Authorization Check: Only Admin or the event owner can view the details
    if current_user.role != "admin" and db_event.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this event")
        
    return db_event

# Add PUT/DELETE endpoints here and protect them based on ownership/admin status