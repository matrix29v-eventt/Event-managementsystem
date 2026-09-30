from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required
from app.models.models import Client
from app.schemas.schemas import ClientBookingDetail
from app.notifications import send_booking_confirmation

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "/my-bookings",
    response_model=List[ClientBookingDetail],
    summary="Get Detailed Bookings for Logged-in Client",
)
def read_my_bookings(
    db: Session = Depends(get_db), current_client: Client = Depends(get_current_client)
):
    # Use the ID retrieved by the token to fetch relevant detailed bookings
    bookings = crud.get_bookings_by_client_id(db, client_id=current_client.id)
    return bookings


@router.get(
    "/admin/details",
    response_model=List[schemas.BookingDetail],
    summary="ADMIN: Get All Detailed Bookings",
)
def get_admin_booking_details(
    db: Session = Depends(get_db),
    # 💡 SECURED: Only Admin can access this full dataset
    current_user=Depends(role_required("admin")),
    skip: int = 0,
    limit: int = 100,
):
    details = crud.get_all_bookings_details(db, skip=skip, limit=limit)
    return details


KNOWN_EVENT_COSTS = {
    "Wedding Reception": 15000,
    "Alumni Gathering": 8000,
    "Annual Fest": 12000,
    "Product Launch": 9500,
    "Company Retreat": 5000,
}


# POLICY: Authenticated (Creation)
@router.post("/", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_client),
):
    db_event = crud.get_event(db, event_id=booking.event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.name in KNOWN_EVENT_COSTS:
        expected_cost = KNOWN_EVENT_COSTS[db_event.name]
        if abs(booking.service_cost - expected_cost) > expected_cost * 0.1:
            raise HTTPException(
                status_code=400,
                detail=f"Service cost {booking.service_cost} does not match expected cost {expected_cost} for {db_event.name}",
            )
    db_booking = crud.create_booking(db=db, booking=booking)

    try:
        db_client = crud.get_client(db, client_id=db_event.client_id)
        db_venue = crud.get_venue(db, db_event.venue_id)
        db_vendor = crud.get_vendor(db, booking.vendor_id)
        if db_client and db_venue and db_vendor:
            send_booking_confirmation(
                client_email=db_client.email,
                client_name=db_client.name,
                event_name=db_event.name,
                event_date=str(db_event.date),
                venue_name=db_venue.name,
                vendor_name=db_vendor.name,
                cost=booking.service_cost,
                booking_id=db_booking.id,
            )
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return db_booking


# POLICY: Admin Only (Read All/Management)
@router.get("/", response_model=List[schemas.Booking])
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),
):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings


# POLICY: Admin Only (Read Single)
@router.get("/{booking_id}", response_model=schemas.Booking)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required("admin")),
):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Client/Admin Delete Booking",
)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client),
):
    db_booking = crud.get_booking(db, booking_id=booking_id)

    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Fetch the associated event to check ownership
    db_event = crud.get_event(db, event_id=db_booking.event_id)

    # 💡 Authorization Check: Must be Admin OR the owner of the event linked to the booking
    if current_client.role != "admin" and db_event.client_id != current_client.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this booking."
        )

    # Execute Delete
    crud.delete_booking(db, booking_id=booking_id)

    # Return 204 No Content for a successful deletion
    return Response(status_code=status.HTTP_204_NO_CONTENT)
