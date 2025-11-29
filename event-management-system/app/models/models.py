# app/models/models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

# -------------------------------
# Clients
# -------------------------------
# ... (imports)

# -------------------------------
# Clients
# -------------------------------
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True) # Add index
    phone = Column(String, nullable=True)
    
    # CHANGE: Rename 'password' to 'hashed_password' and add 'role'
    hashed_password = Column(String, nullable=False) # MUST be nullable=False for secure auth
    role = Column(String, default="client", nullable=False) # New column for authorization

    events = relationship("Event", back_populates="client")

# ... (Other models remain the same)
# -------------------------------
# Venues
# -------------------------------
class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    events = relationship("Event", back_populates="venue")


# -------------------------------
# Vendors
# -------------------------------
class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    contact = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="vendor")


# -------------------------------
# Events
# -------------------------------
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)

    client = relationship("Client", back_populates="events")
    venue = relationship("Venue", back_populates="events")
    bookings = relationship("Booking", back_populates="event")
    payments = relationship("Payment", back_populates="event")


# -------------------------------
# Bookings
# -------------------------------
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    service_cost = Column(Float, nullable=False)

    event = relationship("Event", back_populates="bookings")
    vendor = relationship("Vendor", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")


# -------------------------------
# Payments
# -------------------------------
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    event = relationship("Event", back_populates="payments")
    booking = relationship("Booking", back_populates="payments")
