from typing import List

from crud.users import crud_users
from database.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from schemas import users as schema
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schema.User])
def get_users(db: Session = Depends(get_db)):
    return crud_users.get_all(db)


@router.get("/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.get(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id of {user_id} not found."
        )
    return db_user


@router.post("/", response_model=schema.User)
def add_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud_users.create(db, user)


@router.patch("/{user_id}", response_model=schema.User)
def update_user(user_id: int, user: schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_users.update(db, user_id, user)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id of {user_id} not found."
        )
    return db_user


@router.delete("/{user_id}", response_model=schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.delete(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id of {user_id} not found."
        )
    return db_user
