from sqlalchemy.orm import Session
import models
import schemas
from security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """Fetches a user by there email address"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Creates a new user in the database"""

    #hashing the password
    hashed_password = get_password_hash(user.password)

    #creating a new User model instace
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password, role="user")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
