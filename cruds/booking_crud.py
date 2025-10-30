from pickletools import int4
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException,status
import models
from routers import bookins
import schemas
from . import event_crud

def create_boking(db: Session, booking:schemas.BookingCreate, user_id:int):
    """
    Creates a new booking for a user.
    """

    #get the event user tring to booking
    db_event = event_crud.get_event(db, event_id=booking.event_id)

    # Check if the event exists
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event Not Found')

    # Check if there are enough available seats
    if db_event.available_seats < booking.number_of_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough available seats"
        )

    # if all checks pass, create the booking
    db_booking = models.Booking(
        event_id = booking.event_id,
        number_of_seats= booking.number_of_seats,
        user_id= user_id
    )

    # Descrese the available seats for the event
    db_event.available_seats -= booking.number_of_seats

    db.add(db_booking)
    db.add(db_event)
    db.commit()
    db.refresh(db_booking)

    return db_booking

def get_user_bookings(db: Session, user_id: int):
    """ Gets all booking for a specific user. """

    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

def get_all_booking(db: Session, skip: int = 0, limit: int = 100):
    """ Gets all booking in the system. (Admin only) """
    return db.query(models.Booking).options(
        joinedload(models.Booking.event),  # You already have this
        joinedload(models.Booking.user)   # <-- ADD THIS LINE
    ).offset(skip).limit(limit).all()

# --- Get booking by ID ----
def get_booking(db: Session, booking_id:int):
    """
    Gets a single booking ID.
    """
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def cancel_booking(db: Session, booking_id: int, user_id: int):
    """
    Cancels a booking for a user.
    """

    # 2. Modify the query to eagerly load the 'event'
    db_booking = db.query(models.Booking).options(
        joinedload(models.Booking.event)
    ).filter(
        models.Booking.id == booking_id,
        models.Booking.user_id == user_id
    ).first()

    # 3. Check if it exists
    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    # 4. Create the snapshot *before* deleting
    booking_snapshot = schemas.Booking.model_validate(db_booking)

    # 5. Get the event (it's already loaded, no new query needed)
    db_event = db_booking.event 

    if db_event:
        db_event.available_seats += db_booking.number_of_seats
        db.add(db_event)

    # 6. Delete the booking
    db.delete(db_booking)
    db.commit()

    # 7. Return the Pydantic snapshot
    return booking_snapshot