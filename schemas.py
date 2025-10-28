from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr  
    name: str | None = None

# Schema for CREATING a user 
class UserCreate(UserBase):
    password: str  

# Schema for READING a user 
class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    email: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str