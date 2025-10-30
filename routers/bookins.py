from turtle import mode
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from jinja2 import runtime
from sqlalchemy.orm import Session
from starlette.routing import Router
import ai_utils
import schemas
from cruds import booking_crud
from database import get_db
from auth import get_current_admin_user, get_current_user
import models

router = APIRouter(
    prefix="/api/bookings",
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

# === Get ALL BOOKING (ADMIN ONMLY)====
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

# === Cancel BOOKING (user) ===
@router.delete("/{booking_id}", response_model=schemas.Booking)
def delete_booking (
    booking_id:int,
    db: Session =  Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """ Cancel a booking. A user can only cancel their own bookings """

    try:
        cancelled_booking = booking_crud.cancel_booking(
            db= db, booking_id= booking_id, user_id=current_user.id
        )

        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "success":True,
            "status_code":status.HTTP_200_OK,
            "message": "Booking cancelled successfully",
            "booking":cancelled_booking.model_dump(mode='json')
        })
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={
            "success": False,
            "status_code": e.status_code,
            "message": e.detail
        })
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"An unexpected error occurred: {str(e)}"
        })

# AI BOOKING SUMMERY
@router.get("/me/summary" , response_model=schemas.AIBookingSummary)
def get_ai_booking_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """ Generate a natural language summery of the user's bookings """
    
    #fetch user's booking
    bookings = booking_crud.get_user_bookings(db, user_id=current_user.id)

    #Convert SQLAlchemy objects to Pydantic models (dictionaries)
    bookings_data = [schemas.Booking.model_validate(b).model_dump() for b in bookings]

    # Generate the summary
    summary = ai_utils.generate_booking_summary(bookings_data)

    if summary.startswith("Error:"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=summary)
    
    return {"summary": summary}
