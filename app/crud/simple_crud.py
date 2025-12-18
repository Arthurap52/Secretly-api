from sqlalchemy.orm import Session
from app.models.group import Group
from app.models.participant import Participant
from app.models.draw import Draw
from app.schemas.group import GroupCreate, GroupUpdate
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from typing import List, Optional
import random


def create_group(db: Session, group: GroupCreate) -> Group:
    db_group = Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: int) -> Optional[Group]:
    return db.query(Group).filter(Group.id == group_id).first()

def get_groups(db: Session, limit: int = 100) -> List[Group]:
    return db.query(Group).limit(limit).all()

def update_group(db: Session, group_id: int, group: GroupUpdate) -> Optional[Group]:
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group:
        update_data = group.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_group, field, value)
        db.commit()
        db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int) -> bool:
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

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

def get_all_participants(db: Session, limit: int = 100) -> List[Participant]:
    return db.query(Participant).limit(limit).all()

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

def create_draw(db: Session, draw: Draw) -> Draw:
    db.add(draw)
    db.commit()
    db.refresh(draw)
    return draw

def get_draw(db: Session, draw_id: int) -> Optional[Draw]:
    return db.query(Draw).filter(Draw.id == draw_id).first()

def get_draws_by_group(db: Session, group_id: int) -> List[Draw]:
    return db.query(Draw).filter(Draw.group_id == group_id).all()

def perform_group_draw(db: Session, group_id: int) -> List[Draw]:
    participants = get_participants_by_group(db, group_id)
    
    if len(participants) < 2:
        raise ValueError("At least 2 participants are required to hold the raffle.")
    
    db.query(Draw).filter(Draw.group_id == group_id).delete()
    
    participant_list = participants.copy()
    random.shuffle(participant_list)
    
    draws = []
    
    for i, participant in enumerate(participant_list):
        next_participant = participant_list[(i + 1) % len(participant_list)]
        
        draw = Draw(
            group_id=group_id,
            drawn_by_id=participant.id,
            drawn_to_id=next_participant.id
        )
        
        created_draw = create_draw(db, draw)
        draws.append(created_draw)
    
    return draws

def get_draw_summary(db: Session, group_id: int) -> dict:
    draws = get_draws_by_group(db, group_id)
    
    draw_results = []
    for draw in draws:
        draw_results.append({
            "id": draw.id,
            "group_id": draw.group_id,
            "drawn_by_id": draw.drawn_by_id,
            "drawn_to_id": draw.drawn_to_id,
            "created_at": draw.created_at,
            "drawn_by_name": draw.drawn_by_participant.name,
            "drawn_to_name": draw.drawn_to_participant.name
        })
    
    return {
        "group_id": group_id,
        "total_draws": len(draws),
        "draws": draw_results
    }
