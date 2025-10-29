from pickletools import int4
from sqlalchemy.orm import Session, session
from fastapi import HTTPException,status
import models
import schemas
from . import event_crud

def create_boking(db: session, booking:schemas.BookingCreate, user_id:int):
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
