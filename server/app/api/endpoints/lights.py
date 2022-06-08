from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.schemas.light_cmd import LightCommand, LightCommandCreate, LightCommandUpdate
from app import dependencies

router = APIRouter()

@router.get('/commands', response_model=List[LightCommand])
def get_light_commands(db: Session = Depends(dependencies.get_db)):
    light_cmds = crud.light_cmd.get_multi(db=db)
    return light_cmds

@router.post('/commands', response_model=LightCommand)
def add_light_command(command_in: LightCommandCreate, db: Session = Depends(dependencies.get_db)):
    command = crud.light_cmd.create(db=db, obj_in=command_in)
    return command

@router.put('/commands/{id}', response_model=LightCommand)
def update_light_command(id: int, command_in: LightCommandUpdate, db: Session = Depends(dependencies.get_db)):
    cmd = crud.light_cmd.get(db=db, id=id)

    if not cmd:
        raise HTTPException(
            status_code=400, detail=f"Light command with ID: {id} not found."
        )
    updated_cmd = crud.light_cmd.update(db=db, db_obj=cmd, obj_in=command_in)
    # db.commit()
    return updated_cmd

@router.delete('/commands/{id}', response_model=LightCommand)
def delete_light_command(id: int, db=Depends(dependencies.get_db)):
    command = crud.light_cmd.remove(db=db, id=id)
    return command