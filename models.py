from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    
    #-- relationship to Event model---
    # events = relationship("Event", back_populates="creator")
    
    # We will add roles (admin/user) later
