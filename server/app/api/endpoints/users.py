
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List

from app.schemas.user import User, UserCreate
from app.models.user import User
from fastapi import APIRouter
from app import dependencies
from sqlalchemy.orm import Session
from app import crud


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users/", response_model=User, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[User], tags=["users"])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # users = crud
    return users


@router.get("/users/{user_id}", response_model=User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.delete_user(db,user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return


@router.put("/users/{user_id}", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.update_user(db, user_id)
    return db_user
