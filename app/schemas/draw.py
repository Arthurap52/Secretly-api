from pydantic import BaseModel
from datetime import datetime
from typing import List

class DrawBase(BaseModel):
    group_id: int
    drawn_by_id: int
    drawn_to_id: int

class DrawCreate(DrawBase):
    pass

class DrawOut(DrawBase):
    id: int
    created_at: datetime
    drawn_by_name: str
    drawn_to_name: str
    
    class Config:
        from_attributes = True

class DrawSummary(BaseModel):
    group_id: int
    total_draws: int
    draws: List[DrawOut] = []

