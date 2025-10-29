from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.routing import Router
import schemas
from cruds import booking_crud
from database import get_db
from auth import get_current_admin_user, get_current_user
import models

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/",response_model=schemas.Booking)
def create_new_booking(
    booking:schemas.BookingCreate,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """ Create a new booking
    A user must be logged in to make a booking.
     """

    try:
        return booking_crud.create_boking(db=db, booking= booking, user_id=current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get event created by the user
@router.get("/me/", response_model=list[schemas.Booking])
def read_user_bookings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Get a list of all booking made by the currently logged-in user.
    """

    return booking_crud.get_user_bookings(db=db, user_id=current_user.id)

# === New Get ALL BOOKING (ADMIN ONMLY)====
@router.get("/all", response_model=list[schemas.Booking])
def read_all_bookings(
    skip: int =0, limit:int =100 , 
    db: Session = Depends(get_db), 
    admin_user:models.User = Depends(get_current_admin_user)):
    """ Get a list of all booking in the system
    This is accessible only to the admin
     """
    
    booking = booking_crud.get_all_booking(db, skip=skip, limit=limit)
    return booking