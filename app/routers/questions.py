from typing import List

from crud.questions import crud_questions
from database.session import get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from schemas import questions as schema
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[schema.Question])
def get_questions(db: Session = Depends(get_db)):
    return crud_questions.get_all(db)


@router.get("/{id}", response_model=schema.Question)
def get_question(id: int, db: Session = Depends(get_db)):
    db_question = crud_questions.get(db, id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with id of {id} not found."
        )
    return db_question


@router.post("/", response_model=schema.Question)
def add_question(question: schema.QuestionCreate, db: Session = Depends(get_db)):
    return crud_questions.create(db, question)


@router.delete("/{id}", response_model=schema.Question)
def delete_question(id: int, db: Session = Depends(get_db)):
    db_question = crud_questions.delete(db, id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with id of {id} not found."
        )
    return db_question
