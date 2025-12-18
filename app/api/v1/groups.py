from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.crud.simple_crud import (
    create_group as crud_create_group,
    get_group as crud_get_group,
    get_groups as crud_get_groups,
    update_group as crud_update_group,
    delete_group as crud_delete_group,
)
from app.schemas.group import GroupCreate, GroupUpdate, GroupOut
from typing import List

router = APIRouter()

@router.post("/", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    return crud_create_group(db, group)

@router.get("/", response_model=List[GroupOut])
def get_groups_endpoint(limit: int = 100, db: Session = Depends(get_db)):
    return crud_get_groups(db, limit=limit)

@router.get("/{group_id}", response_model=GroupOut)
def get_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    group = crud_get_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/{group_id}", response_model=GroupOut)
def update_group_endpoint(group_id: int, group: GroupUpdate, db: Session = Depends(get_db)):
    updated_group = crud_update_group(db, group_id, group)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_endpoint(group_id: int, db: Session = Depends(get_db)):
    success = crud_delete_group(db, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")

