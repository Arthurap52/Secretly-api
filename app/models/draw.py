from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Draw(Base):
    __tablename__ = "draws"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    drawn_by_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    drawn_to_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    group = relationship("Group", back_populates="draws")
    drawn_by_participant = relationship("Participant", foreign_keys=[drawn_by_id], back_populates="drawn_by")
    drawn_to_participant = relationship("Participant", foreign_keys=[drawn_to_id], back_populates="draws_to")

