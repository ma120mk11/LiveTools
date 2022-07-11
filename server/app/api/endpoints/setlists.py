from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.schemas.light_cmd import LightCommand, LightCommandCreate, LightCommandUpdate
from app import dependencies
from app.live_engine import engine
from app.schemas.setlist import SetlistCreate

router = APIRouter()

@router.get("")
def get_setlists(db: Session = Depends(dependencies.get_db)):
    return crud.setlist.get_multi(db=db)

@router.get("/{id}")
def get_setlists(id: int, db: Session = Depends(dependencies.get_db)):
    return crud.setlist.get(db=db, id=id)

@router.post("")
def create_setlist(setlist: SetlistCreate, db: Session = Depends(dependencies.get_db)):
    setlist_db = crud.setlist.create(db=db, obj_in=setlist)
    return setlist_db

@router.delete("/{id}")
def delete_setlist(id: int, db: Session = Depends(dependencies.get_db)):
    crud.setlist.remove(db=db, id=id)