from typing import List, Optional
from database.models import Choice

from crud.choices import crud_choices
from database.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from schemas import choices as schema
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/choices", tags=["choices"])


@router.get("/", response_model=List[schema.Choice])
def get_choices(question_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud_choices.get_all(db, question_id)


@router.get("/{id}", response_model=schema.Choice)
def get_choice(id: int, db: Session = Depends(get_db)):
    db_choice = crud_choices.get(db, id)
    if db_choice is None:
        raise HTTPException(
            status_code=404,
            detail=f"Choice with id of {id} not found."
        )
    return db_choice


@router.post("/", response_model=schema.Choice)
def add_choice(choice: schema.ChoiceCreate, db: Session = Depends(get_db)):
    db_choice = crud_choices.create(db, choice)

    if type(db_choice) == Choice:
        return db_choice

    # Invalid creation
    else:
        raise HTTPException(
            status_code=400,
            detail=db_choice["msg"]
        )


@router.delete("/{id}", response_model=schema.Choice)
def delete_question(id: int, db: Session = Depends(get_db)):
    db_choice = crud_choices.delete(db, id)
    if db_choice is None:
        raise HTTPException(

            status_code=404,
            detail=f"Choice with id of {id} not found."
        )
    return db_choice
