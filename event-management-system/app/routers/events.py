from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.models.models import Client
from app.auth import get_current_client

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=schemas.Event, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client),
):
    if current_user.role != "admin" and event.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create an event for another client.",
        )
    return crud.create_event(db=db, event=event)


@router.get("/", response_model=List[schemas.Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client),
):
    if current_user.role == "client":
        return crud.get_events_by_client(
            db, client_id=current_user.id, skip=skip, limit=limit
        )
    return crud.get_events(db, skip=skip, limit=limit)


@router.get("/{event_id}", response_model=schemas.Event)
def read_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_client),
):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if current_user.role != "admin" and db_event.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this event",
        )
    return db_event
