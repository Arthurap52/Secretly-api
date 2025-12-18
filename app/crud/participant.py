from sqlalchemy.orm import Session
from app.models.participant import Participant
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from typing import List, Optional

def create_participant(db: Session, participant: ParticipantCreate) -> Participant:
    db_participant = Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participant(db: Session, participant_id: int) -> Optional[Participant]:
    return db.query(Participant).filter(Participant.id == participant_id).first()

def get_participants_by_group(db: Session, group_id: int) -> List[Participant]:
    return db.query(Participant).filter(Participant.group_id == group_id).all()

def get_all_participants(db: Session, skip: int = 0, limit: int = 100) -> List[Participant]:
    return db.query(Participant).offset(skip).limit(limit).all()

def update_participant(db: Session, participant_id: int, participant: ParticipantUpdate) -> Optional[Participant]:
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant:
        update_data = participant.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_participant, field, value)
        db.commit()
        db.refresh(db_participant)
    return db_participant

def delete_participant(db: Session, participant_id: int) -> bool:
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant:
        db.delete(db_participant)
        db.commit()
        return True
    return False

