# # app/routers/bookings.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.db import get_db
# from app.crud import crud
# from app.schemas import schemas
# from app.auth import get_current_client, role_required

# router = APIRouter(
#     prefix="/bookings",
#     tags=["Bookings"]
# )

# # POLICY: Authenticated (Creation) - assuming client/admin can create bookings
# @router.post("/", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
# def create_booking(
#     booking: schemas.BookingCreate, 
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_client) # Requires any valid token
# ):
#     # You would typically perform checks here:
#     # 1. Does the event_id belong to current_user (if client)?
#     # 2. Does the vendor_id exist?
#     return crud.create_booking(db=db, booking=booking)

# # POLICY: Admin Only (Read All/Management)
# @router.get("/", response_model=List[schemas.Booking])
# def read_bookings(
#     skip: int = 0, 
#     limit: int = 100, 
#     db: Session = Depends(get_db),
#     current_user = Depends(role_required("admin")) # Requires admin role
# ):
#     bookings = crud.get_bookings(db, skip=skip, limit=limit)
#     return bookings

# # POLICY: Admin Only (Read Single)
# @router.get("/{booking_id}", response_model=schemas.Booking)
# def read_booking(
#     booking_id: int, 
#     db: Session = Depends(get_db),
#     current_user = Depends(role_required("admin")) # Requires admin role
# ):
#     db_booking = crud.get_booking(db, booking_id=booking_id)
#     if db_booking is None:
#         raise HTTPException(status_code=404, detail="Booking not found")
#     return db_booking

# # Add PUT/DELETE endpoints here and protect them with role_required("admin")

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import crud
from app.schemas import schemas
from app.auth import get_current_client, role_required
from app.models.models import Client # Import Client model
from app.schemas.schemas import ClientBookingDetail

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)



@router.get("/my-bookings", response_model=List[ClientBookingDetail], summary="Get Detailed Bookings for Logged-in Client")
def read_my_bookings(
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client)
):
    # Use the ID retrieved by the token to fetch relevant detailed bookings
    bookings = crud.get_bookings_by_client_id(db, client_id=current_client.id)
    return bookings
# app/routers/bookings.py

# ... (Existing imports) ...

# ... (Existing router definition and endpoints) ...

@router.get("/admin/details", response_model=List[schemas.BookingDetail], summary="ADMIN: Get All Detailed Bookings")
def get_admin_booking_details(
    db: Session = Depends(get_db),
    # 💡 SECURED: Only Admin can access this full dataset
    current_user = Depends(role_required("admin")), 
    skip: int = 0, limit: int = 100
):
    details = crud.get_all_bookings_details(db, skip=skip, limit=limit)
    return details


# POLICY: Authenticated (Creation)
@router.post("/", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: schemas.BookingCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_client)
):
    return crud.create_booking(db=db, booking=booking)

# POLICY: Admin Only (Read All/Management)
@router.get("/", response_model=List[schemas.Booking])
def read_bookings(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    bookings = crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

# POLICY: Admin Only (Read Single)
@router.get("/{booking_id}", response_model=schemas.Booking)
def read_booking(
    booking_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Client/Admin Delete Booking")
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client)
):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Fetch the associated event to check ownership
    db_event = crud.get_event(db, event_id=db_booking.event_id)
    
    # 💡 Authorization Check: Must be Admin OR the owner of the event linked to the booking
    if current_client.role != "admin" and db_event.client_id != current_client.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this booking.")

    # Execute Delete
    crud.delete_booking(db, booking_id=booking_id)
    
    # Return 204 No Content for a successful deletion
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
