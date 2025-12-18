from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.crud.simple_crud import (
    perform_group_draw as crud_perform_group_draw,
    get_draws_by_group as crud_get_draws_by_group,
    get_draw_summary as crud_get_draw_summary,
    get_group as crud_get_group,
)
from app.schemas.draw import DrawOut, DrawSummary
from typing import List

router = APIRouter()

@router.post("/group/{group_id}/perform", response_model=List[DrawOut], status_code=status.HTTP_201_CREATED)
def perform_group_draw_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    existing_draws = crud_get_draws_by_group(db, group_id)
    if existing_draws:
        raise HTTPException(status_code=400, detail="There is already a draw for this group.")
    
    try:
        draws = crud_perform_group_draw(db, group_id)
        result = []
        for draw in draws:
            result.append(DrawOut(
                id=draw.id,
                group_id=draw.group_id,
                drawn_by_id=draw.drawn_by_id,
                drawn_to_id=draw.drawn_to_id,
                created_at=draw.created_at,
                drawn_by_name=draw.drawn_by_participant.name,
                drawn_to_name=draw.drawn_to_participant.name
            ))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/group/{group_id}", response_model=List[DrawOut])
def get_draws_by_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    draws = crud_get_draws_by_group(db, group_id)
    result = []
    for draw in draws:
        result.append(DrawOut(
            id=draw.id,
            group_id=draw.group_id,
            drawn_by_id=draw.drawn_by_id,
            drawn_to_id=draw.drawn_to_id,
            created_at=draw.created_at,
            drawn_by_name=draw.drawn_by_participant.name,
            drawn_to_name=draw.drawn_to_participant.name
        ))
    return result

@router.get("/group/{group_id}/summary", response_model=DrawSummary)
def get_draw_summary_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    summary = crud_get_draw_summary(db, group_id)
    return summary

