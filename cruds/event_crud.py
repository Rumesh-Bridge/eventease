from sqlalchemy.orm import Session
import models
import schemas

def get_event(db: Session, event_id: int):
    """Get a single event by its ID."""
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of all events."""
    return db.query(models.Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate, creator_id: int):
    """Create a new event in the database."""
    
    # When creating an event, available_seats starts equal to total_seats
    db_event = models.Event(
        **event.model_dump(),  
        available_seats=event.total_seats, 
        creator_id=creator_id
    )
    
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventCreate):
    """Update an existing event. Returns the updated event or None if not found."""
    db_event = get_event(db, event_id)
    if not db_event:
        return None

    # Preserve reserved seats when changing total_seats
    previous_total = db_event.total_seats
    previous_available = db_event.available_seats

    update_data = event_update.model_dump()
    for field_name, value in update_data.items():
        setattr(db_event, field_name, value)

    if event_update.total_seats != previous_total:
        reserved = max(0, previous_total - previous_available)
        db_event.available_seats = max(0, event_update.total_seats - reserved)

    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    """Delete an event by ID. Returns True if deleted, False if not found."""
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True