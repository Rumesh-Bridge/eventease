import datetime
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

class User(UserBase):
    id:int
    role:str 

    class Config:
        from_attributes = True

# === NEW EVENT SCHEMA ===
class EventBase(BaseModel):
    title:str 
    description:str | None = None
    location:str 
    date_time:datetime.datetime
    total_seats:int 

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id:int
    available_seats:int 
    creator_id: int

    class Config:
        from_attributes =True

# === NEW BOOKING SCHEMA ====

class BookingBase(BaseModel):
    event_id: int
    number_of_seats: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int
    booking_time: datetime.datetime
    event: Event
    user:User  

    class Config:
        from_attributes = True

# === AI Schemas ===

class AIDescriptionPrompt(BaseModel):
    prompt: str

class AIDescriptionResponse(BaseModel):
    description: str

class AIBookingSummary(BaseModel):
    summary: str

class AIChatRequest(BaseModel):
    query: str

class AIChatResponse(BaseModel):
    response: str