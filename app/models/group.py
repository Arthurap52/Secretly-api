from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    participants = relationship("Participant", back_populates="group", cascade="all, delete-orphan")
    draws = relationship("Draw", back_populates="group", cascade="all, delete-orphan")

