from sqlalchemy.orm import Session
from app.models.draw import Draw
from app.models.participant import Participant
from app.schemas.draw import DrawCreate
from typing import List, Optional
import random

def create_draw(db: Session, draw: DrawCreate) -> Draw:
    db_draw = Draw(**draw.dict())
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw

def get_draw(db: Session, draw_id: int) -> Optional[Draw]:
    return db.query(Draw).filter(Draw.id == draw_id).first()

def get_draws_by_group(db: Session, group_id: int) -> List[Draw]:
    return db.query(Draw).filter(Draw.group_id == group_id).all()

def perform_group_draw(db: Session, group_id: int) -> List[Draw]:
    participants = db.query(Participant).filter(Participant.group_id == group_id).all()
    
    if len(participants) < 2:
        raise ValueError("At least 2 participants are required to hold the raffle.")
    
    db.query(Draw).filter(Draw.group_id == group_id).delete()
    
    participant_list = [p.id for p in participants]
    random.shuffle(participant_list)
    
    draws = []
    
    for i, participant_id in enumerate(participant_list):
        next_participant_id = participant_list[(i + 1) % len(participant_list)]
        
        draw = Draw(
            group_id=group_id,
            drawn_by_id=participant_id,
            drawn_to_id=next_participant_id
        )
        db.add(draw)
        draws.append(draw)
    
    db.commit()
    
    for draw in draws:
        db.refresh(draw)
    
    return draws

def get_draw_summary(db: Session, group_id: int) -> dict:
    draws = get_draws_by_group(db, group_id)
    
    return {
        "group_id": group_id,
        "total_draws": len(draws),
        "draws": draws
    }

