from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models
from cruds import user_crud
from database import get_db
from security import verify_token

# This tells FastAPI that the token URL is /users/login/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Verifies a token and returns the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify the token
    email = verify_token(token, credentials_exception)
    
    # Get the user from the database
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin_user(current_user: models.User = Depends(get_current_user)):
    """
    A dependency that checks if the current user is an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user