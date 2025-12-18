from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class ParticipantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None

class ParticipantCreate(ParticipantBase):
    group_id: int

class ParticipantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None

class ParticipantOut(ParticipantBase):
    id: int
    group_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

