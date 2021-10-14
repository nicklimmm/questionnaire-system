from enum import Enum
from pydantic import BaseModel
from schemas.alloptional import AllOptional


class QuestionType(str, Enum):
    textbox = 'textbox'
    checkbox = 'checkbox'
    radio = 'radio'


class QuestionCreate(BaseModel):
    description: str
    type: QuestionType


class QuestionUpdate(BaseModel):
    pass


class Question(QuestionCreate):
    id: int

    class Config:
        orm_mode = True
