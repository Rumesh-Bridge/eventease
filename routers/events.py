from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import ai_utils
import schemas
from cruds import event_crud
from database import get_db
from auth import get_current_admin_user  
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

@router.get("/{event_id}", response_model=schemas.Event)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """
    Get a single event by its ID. Public endpoint.
    """
    event = event_crud.get_event(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event_update: schemas.EventCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Update an existing event. Admin-only.
    """
    updated = event_crud.update_event(db, event_id=event_id, event_update=event_update)
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
        
    return updated

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete an event by ID. Admin-only.
    """
    deleted = event_crud.delete_event(db, event_id=event_id)
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": "Event not found"
        })
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Event deleted successfully"
    })

@router.post("/generate_description/", response_model=schemas.AIDescriptionResponse)
def get_ai_description(
    prompt:schemas.AIDescriptionPrompt,
    admin_user: models.User = Depends(get_current_admin_user)
):
    """
    Generates a proffessional event description from a short prompt.
    This is assessible only to admin usres.
    """
    description = ai_utils.generate_event_description(prompt.prompt)

    if (description.startswith("Error: ")):
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=description)
    
    return {"description": description}