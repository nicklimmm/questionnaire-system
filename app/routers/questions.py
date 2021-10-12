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


@router.get("/{question_id}", response_model=schema.Question)
def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud_questions.get(db, question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with id of {question_id} not found."
        )
    return db_question


@router.post("/", response_model=schema.Question)
def add_question(question: schema.QuestionCreate, db: Session = Depends(get_db)):
    return crud_questions.create(db, question)


@router.patch("/{question_id}", response_model=schema.Question)
def update_question(question_id: int, question: schema.QuestionUpdate, db: Session = Depends(get_db)):
    db_question = crud_questions.update(db, question_id, question)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with id of {question_id} not found."
        )
    return db_question


@router.delete("/{question_id}", response_model=schema.Question)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud_questions.delete(db, question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question with id of {question_id} not found."
        )
    return db_question
