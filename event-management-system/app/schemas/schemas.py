from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


# -------------------------------
# Clients
# -------------------------------
class ClientBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ClientCreate(ClientBase):
    password: str


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class Client(ClientBase):
    id: int
    role: str
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Venues
# -------------------------------
class VenueBase(BaseModel):
    name: str
    location: str
    capacity: int


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None


class Venue(VenueBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Vendors
# -------------------------------
class VendorBase(BaseModel):
    name: str
    service_type: str
    contact: str


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    service_type: Optional[str] = None
    contact: Optional[str] = None


class Vendor(VendorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Events
# -------------------------------
class EventBase(BaseModel):
    name: str
    date: date
    client_id: int
    venue_id: int


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Bookings
# -------------------------------
class BookingBase(BaseModel):
    event_id: int
    vendor_id: int
    service_cost: float


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Payments
# -------------------------------
class PaymentBase(BaseModel):
    event_id: int
    booking_id: Optional[int] = None
    amount: float
    method: str
    status: str
    date: date


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    event_id: Optional[int] = None
    booking_id: Optional[int] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[str] = None
    date: Optional[date] = None


class Payment(PaymentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Authentication Schemas (FIXED)
# -------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
    client_id: Optional[int] = None


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    client_id: Optional[int] = None  # 💡 FIX: ID inside the JWT payload


class Login(BaseModel):
    email: str
    password: str


# -------------------------------
# ADMIN DETAIL SCHEMAS
# -------------------------------
class BookingDetail(BaseModel):
    # Booking Data
    booking_id: int
    service_cost: float

    # Event Data
    event_id: int
    event_name: str
    event_date: date

    # Client Data
    client_id: int
    client_name: str
    client_email: str

    # Vendor Data
    vendor_name: str
    service_type: str

    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# CLIENT BOOKING DETAILS
# -------------------------------
class ClientBookingDetail(BaseModel):
    booking_id: int
    service_cost: float

    # Event/Venue Data
    event_name: str
    event_date: date
    venue_name: str

    # Vendor Data
    vendor_name: str
    service_type: str

    model_config = ConfigDict(from_attributes=True)
