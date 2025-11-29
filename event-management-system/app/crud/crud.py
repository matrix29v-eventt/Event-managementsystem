# # app/crud/crud.py
# from sqlalchemy.orm import Session
# # Imports all models needed for CRUD operations
# from app.models.models import Client, Venue, Vendor, Event, Booking, Payment
# # Imports all Pydantic schemas for data validation
# from app.schemas.schemas import ClientCreate, VenueCreate, VendorCreate, EventCreate, BookingCreate, PaymentCreate
# from passlib.context import CryptContext
# # 💡 FIX: Ensure datetime and timezone are imported for V2 compatibility
# from datetime import datetime, timezone 

# # Password Hashing Context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # --- Utility Functions ---

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# # --- CRUD Operations ---

# # ==========================
# # CLIENT CRUD
# # ==========================
# def get_client(db: Session, client_id: int):
#     return db.query(Client).filter(Client.id == client_id).first()

# def get_client_by_email(db: Session, email: str):
#     # This is the function the auth logic imports. Must be defined here.
#     return db.query(Client).filter(Client.email == email).first()

# def create_client(db: Session, client: ClientCreate, role: str = "client"):
#     hashed_pass = hash_password(client.password)
#     db_client = Client(
#         name=client.name,
#         email=client.email,
#         phone=client.phone,
#         hashed_password=hashed_pass,
#         role=role
#     )
#     db.add(db_client)
#     db.commit()
#     db.refresh(db_client)
#     return db_client

# def get_clients(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Client).offset(skip).limit(limit).all()


# # ==========================
# # VENUE CRUD
# # ==========================
# def get_venue(db: Session, venue_id: int):
#     return db.query(Venue).filter(Venue.id == venue_id).first()

# def create_venue(db: Session, venue: VenueCreate):
#     db_venue = Venue(
#         name=venue.name,
#         location=venue.location,
#         capacity=venue.capacity
#     )
#     db.add(db_venue)
#     db.commit()
#     db.refresh(db_venue)
#     return db_venue

# def get_venues(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Venue).offset(skip).limit(limit).all()


# # ==========================
# # VENDOR CRUD
# # ==========================
# def get_vendor(db: Session, vendor_id: int):
#     return db.query(Vendor).filter(Vendor.id == vendor_id).first()

# def create_vendor(db: Session, vendor: VendorCreate):
#     db_vendor = Vendor(
#         name=vendor.name,
#         service_type=vendor.service_type,
#         # 💡 FIX: Aligns with Vendor model column name 'contact'
#         contact=vendor.contact
#     )
#     db.add(db_vendor)
#     db.commit()
#     db.refresh(db_vendor)
#     return db_vendor

# def get_vendors(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Vendor).offset(skip).limit(limit).all()


# # ==========================
# # EVENT CRUD
# # ==========================
# def get_event(db: Session, event_id: int):
#     return db.query(Event).filter(Event.id == event_id).first()

# def create_event(db: Session, event: EventCreate):
#     db_event = Event(
#         name=event.name,
#         date=event.date,
#         # 💡 FIX: Ensures NotNullViolation for client_id is resolved
#         client_id=event.client_id,
#         venue_id=event.venue_id
#         # Removed non-existent 'description' field
#     )
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event

# def get_events(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Event).offset(skip).limit(limit).all()


# # ==========================
# # BOOKING CRUD
# # ==========================
# def get_booking(db: Session, booking_id: int):
#     return db.query(Booking).filter(Booking.id == booking_id).first()

# def create_booking(db: Session, booking: BookingCreate):
#     db_booking = Booking(
#         # Removed non-existent 'client_id' field from model mapping
#         event_id=booking.event_id,
#         vendor_id=booking.vendor_id,
#         service_cost=booking.service_cost
#     )
#     db.add(db_booking)
#     db.commit()
#     db.refresh(db_booking)
#     return db_booking

# def get_bookings(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Booking).offset(skip).limit(limit).all()


# # ==========================
# # PAYMENT CRUD
# # ==========================
# def get_payment(db: Session, payment_id: int):
#     return db.query(Payment).filter(Payment.id == payment_id).first()

# def create_payment(db: Session, payment: PaymentCreate):
#     db_payment = Payment(
#         event_id=payment.event_id,
#         booking_id=payment.booking_id,
#         amount=payment.amount,
#         # 💡 FIX 1: Use 'method' from schema (not payment_method)
#         method=payment.method,
#         status=payment.status,
#         # 💡 FIX 2: Use 'date' which is the model's column name (not payment_date)
#         date=payment.date 
#     )
#     db.add(db_payment)
#     db.commit()
#     db.refresh(db_payment)
#     return db_payment

# def get_payments(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Payment).offset(skip).limit(limit).all()


# app/crud/crud.py
from sqlalchemy.orm import Session
from app.models.models import Client, Venue, Vendor, Event, Booking, Payment
from app.schemas.schemas import ClientCreate, VenueCreate, VendorCreate, EventCreate, BookingCreate, PaymentCreate
from passlib.context import CryptContext
from datetime import datetime, timezone 

# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ==========================
# CLIENT CRUD
# ==========================
def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first() 

def create_client(db: Session, client: ClientCreate, role: str = "client"):
    hashed_pass = hash_password(client.password)
    db_client = Client(
        name=client.name,
        email=client.email,
        phone=client.phone,
        hashed_password=hashed_pass,
        role=role
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()


# ==========================
# VENUE CRUD
# ==========================
def get_venue(db: Session, venue_id: int):
    return db.query(Venue).filter(Venue.id == venue_id).first()

def create_venue(db: Session, venue: VenueCreate):
    db_venue = Venue(
        name=venue.name,
        location=venue.location,
        capacity=venue.capacity
    )
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

def get_venues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Venue).offset(skip).limit(limit).all()


# ==========================
# VENDOR CRUD
# ==========================
def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = Vendor(
        name=vendor.name,
        service_type=vendor.service_type,
        contact=vendor.contact
    )
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendor).offset(skip).limit(limit).all()


# ==========================
# EVENT CRUD
# ==========================
def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def create_event(db: Session, event: EventCreate):
    db_event = Event(
        name=event.name,
        date=event.date,
        client_id=event.client_id,
        venue_id=event.venue_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()


# ==========================
# BOOKING CRUD
# ==========================
def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def create_booking(db: Session, booking: BookingCreate):
    db_booking = Booking(
        event_id=booking.event_id,
        vendor_id=booking.vendor_id,
        service_cost=booking.service_cost
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()

def get_bookings_by_client_id(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    """Retrieves detailed booking information specific to the client."""
    
    # 💡 FIX: Join multiple tables to get names and details
    query = db.query(
        Booking.id.label("booking_id"),
        Booking.service_cost,
        Event.name.label("event_name"),
        Event.date.label("event_date"),
        Venue.name.label("venue_name"),
        Vendor.name.label("vendor_name"),
        Vendor.service_type
    ).join(Event, Booking.event_id == Event.id)\
     .join(Venue, Event.venue_id == Venue.id)\
     .join(Vendor, Booking.vendor_id == Vendor.id)\
     .filter(Event.client_id == client_id)\
     .offset(skip).limit(limit)
     
    return query.all()


# ==========================
# PAYMENT CRUD
# ==========================
def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        event_id=payment.event_id,
        booking_id=payment.booking_id,
        amount=payment.amount,
        method=payment.method,
        status=payment.status,
        date=payment.date 
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Payment).offset(skip).limit(limit).all()

def get_all_bookings_details(db: Session, skip: int = 0, limit: int = 100):
    """Retrieves detailed booking information including client and event data."""
    
    # 💡 Query joins Bookings, Events, and Clients
    query = db.query(
        Booking.id.label("booking_id"),
        Booking.service_cost,
        Event.id.label("event_id"),
        Event.name.label("event_name"),
        Event.date.label("event_date"),
        Client.id.label("client_id"),
        Client.name.label("client_name"),
        Client.email.label("client_email"),
        Vendor.name.label("vendor_name"),
        Vendor.service_type
    ).join(Event, Booking.event_id == Event.id)\
     .join(Client, Event.client_id == Client.id)\
     .join(Vendor, Booking.vendor_id == Vendor.id)\
     .offset(skip).limit(limit)
     
    # Return as SQLAlchemy Row objects (which FastAPI will convert to JSON)
    return query.all()

def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return True
    return False


