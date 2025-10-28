from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from cruds import event_crud
from database import get_db
from auth import get_current_admin_user  # <-- Import our admin-only dependency
import models

router = APIRouter(
    prefix="/events",
    tags=["Events"]  # This groups them in the /docs
)

@router.post("/", response_model=schemas.Event)
def create_new_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    # This dependency protects the endpoint
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Create a new event. This endpoint is accessible only to admin users.
    """
    return event_crud.create_event(db=db, event=event, creator_id=admin_user.id)


@router.get("/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of all available events. This is a public endpoint.
    """
    events = event_crud.get_events(db, skip=skip, limit=limit)
    return events