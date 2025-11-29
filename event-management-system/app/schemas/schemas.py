# # app/schemas/schemas.py
# from pydantic import BaseModel, ConfigDict, model_validator # ADD ConfigDict and model_validator
# from typing import Optional
# from datetime import date
# from datetime import datetime # Needed for validation

# # -------------------------------
# # Clients
# # -------------------------------
# class ClientBase(BaseModel):
#     name: str
#     email: str
#     phone: Optional[str] = None

# class ClientCreate(ClientBase):
#     # Password is MANDATORY for creation after authentication setup
#     password: str 

# class Client(ClientBase):
#     id: int
#     role: str # Added for authorization response

#     # 💡 V2 Change: Replaced class Config with model_config
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Venues
# # -------------------------------
# class VenueBase(BaseModel):
#     name: str
#     location: str
#     capacity: int

# class VenueCreate(VenueBase):
#     pass

# class Venue(VenueBase):
#     id: int
#     # 💡 V2 Change
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Vendors
# # -------------------------------
# class VendorBase(BaseModel):
#     name: str
#     service_type: str
#     contact: str

# class VendorCreate(VendorBase):
#     pass

# class Vendor(VendorBase):
#     id: int
#     # 💡 V2 Change
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Events
# # -------------------------------
# class EventBase(BaseModel):
#     name: str
#     date: date
#     client_id: int
#     venue_id: int

# class EventCreate(EventBase):
#     # 💡 V2 Change: Updated @root_validator to @model_validator
#     @model_validator(mode='before')
#     @classmethod
#     def validate_event_date(cls, data: dict):
#         """Ensure the event date is not in the past."""
#         # Note: data here is typically a dict from the request body
#         event_date_str = data.get('date')
#         if event_date_str:
#             try:
#                 event_date = datetime.strptime(str(event_date_str), '%Y-%m-%d').date()
#             except ValueError:
#                 raise ValueError("Invalid date format. Use YYYY-MM-DD.")
                
#             if event_date < date.today():
#                 raise ValueError('Event date cannot be in the past.')
#         return data

# class Event(EventBase):
#     id: int
#     # 💡 V2 Change
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Bookings
# # -------------------------------
# class BookingBase(BaseModel):
#     event_id: int
#     vendor_id: int
#     service_cost: float

# class BookingCreate(BookingBase):
#     pass

# class Booking(BookingBase):
#     id: int
#     # 💡 V2 Change
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Payments
# # -------------------------------
# class PaymentBase(BaseModel):
#     event_id: int
#     booking_id: Optional[int] = None
#     amount: float
#     method: str
#     status: str
#     date: date

# class PaymentCreate(PaymentBase):
#     pass

# class Payment(PaymentBase):
#     id: int
#     # 💡 V2 Change
#     model_config = ConfigDict(from_attributes=True)


# # -------------------------------
# # Authentication Schemas (Already V2 compatible, but included for completeness)
# # -------------------------------

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     email: Optional[str] = None
#     role: Optional[str] = None

# class Login(BaseModel):
#     email: str
#     password: str


# app/schemas/schemas.py
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

class Payment(PaymentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------------------------------
# Authentication Schemas (FIXED)
# -------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str
    client_id: int = None # 💡 FIX: Return ID in login response

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    client_id: Optional[int] = None # 💡 FIX: ID inside the JWT payload

class Login(BaseModel):
    email: str
    password: str

# app/schemas/schemas.py (Add this schema near the end)

# -------------------------------
# ADMIN DETAIL SCHEMAS (NEW)
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

    # app/schemas/schemas.py (Add this schema near the BookingDetail schema)

# -------------------------------
# CLIENT BOOKING DETAILS (NEW)
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