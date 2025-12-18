from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    group = relationship("Group", back_populates="participants")
    drawn_by = relationship("Draw", foreign_keys="Draw.drawn_by_id", back_populates="drawn_by_participant")
    draws_to = relationship("Draw", foreign_keys="Draw.drawn_to_id", back_populates="drawn_to_participant")

