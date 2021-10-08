from fastapi import APIRouter, HTTPException
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class QuestionType(str, Enum):
    textbox = 'textbox'
    checkbox = 'checkbox'
    radio = 'radio'


class Question(BaseModel):
    question: str
    questionType: QuestionType


class OptionalQuestion(BaseModel):
    question: Optional[str]
    questionType: Optional[QuestionType]


questions = {}

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/{question_id}")
def get_question(question_id: int) -> Question:
    if question_id not in questions:
        raise HTTPException(
            status_code=404, detail=f"Question with id of {question_id} not found.")
    return questions[question_id]


@router.post("/")
def add_question(question: Question) -> int:
    next_id = len(questions) + 1
    questions[next_id] = question
    return next_id


@router.put("/{question_id}")
def update_question(question_id: int, question: OptionalQuestion) -> int:
    if question_id not in questions:
        raise HTTPException(
            status_code=404, detail=f"Question with id of {question_id} not found.")
    for key, value in question.items():
        questions[question_id][key] = value
    return question_id


@router.delete("/{question_id}")
def delete_question(question_id: int) -> int:
    if question_id not in questions:
        raise HTTPException(
            status_code=404, detail=f"Question with id of {question_id} not found.")
    del questions[question_id]
    return question_id
