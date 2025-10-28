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