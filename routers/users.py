from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from cruds import user_crud  
import models               
import schemas              
from database import get_db
from security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)


@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = user_crud.create_user(db, user=user)
    return new_user


@router.post("/login/", response_model=schemas.Token)
def login_for_access_token(
  
    login_data: schemas.UserLogin, 
    db: Session = Depends(get_db)
):
    """
    Logs in a user and returns a JWT access token.
    """
  
    user = user_crud.get_user_by_email(db, email=login_data.email) 
    
    if not user or not verify_password(login_data.password, user.hashed_password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

