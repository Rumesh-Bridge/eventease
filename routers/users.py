from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from cruds import user_crud  
import models               
import schemas              
from database import get_db

# 1. Create a router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#2. Chnage decorator to @router.post
@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = user_crud.create_user(db, user=user)
    return new_user

#WE will add the /login endpoint later

