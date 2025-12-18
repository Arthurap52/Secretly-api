from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.crud.simple_crud import (
    create_participant as crud_create_participant,
    get_participant as crud_get_participant,
    get_participants_by_group as crud_get_participants_by_group,
    get_all_participants as crud_get_all_participants,
    update_participant as crud_update_participant,
    delete_participant as crud_delete_participant,
    get_group as crud_get_group,
)
from app.schemas.participant import ParticipantCreate, ParticipantUpdate, ParticipantOut
from typing import List

router = APIRouter()

@router.post("/", response_model=ParticipantOut, status_code=status.HTTP_201_CREATED)
def create_participant_endpoint(participant: ParticipantCreate, db: Session = Depends(get_db)):
    group = crud_get_group(db, participant.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return crud_create_participant(db, participant)

@router.get("/", response_model=List[ParticipantOut])
def get_participants_endpoint(limit: int = 100, db: Session = Depends(get_db)):
    return crud_get_all_participants(db, limit=limit)

@router.get("/group/{group_id}", response_model=List[ParticipantOut])
def get_participants_by_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return crud_get_participants_by_group(db, group_id)

@router.get("/{participant_id}", response_model=ParticipantOut)
def get_participant_endpoint(participant_id: int, db: Session = Depends(get_db)):
    participant = crud_get_participant(db, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@router.put("/{participant_id}", response_model=ParticipantOut)
def update_participant_endpoint(participant_id: int, participant: ParticipantUpdate, db: Session = Depends(get_db)):
    updated_participant = crud_update_participant(db, participant_id, participant)
    if not updated_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return updated_participant

@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant_endpoint(participant_id: int, db: Session = Depends(get_db)):
    success = crud_delete_participant(db, participant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Participant not found")

