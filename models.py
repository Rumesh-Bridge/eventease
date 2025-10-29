from pickle import TRUE
from jose.backends import base
from sqlalchemy import Column, Index, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
import datetime

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    
    #-- relationship to Event model---
    events = relationship("Event", back_populates="creator")

    # -- relationship to booking model ---
    bookings = relationship("Booking", back_populates="user")
    
    
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    
    creator_id = Column(Integer, ForeignKey("users.id"))

    #--- relationship to the user---
    creator = relationship("User", back_populates="events")

    #--- realtionship to the booking class--
    bookings = relationship("Booking", back_populates="event")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    number_of_seats = Column(Integer, nullable=False)

   # Foreign key for the user who made the booking
    user_id = Column(Integer, ForeignKey("users.id"))
    # Foreign key for the event being booked
    event_id = Column(Integer, ForeignKey("events.id"))

    #Relationships
    user = relationship("User", back_populates="bookings")
    event = relationship("Event", back_populates="bookings")
