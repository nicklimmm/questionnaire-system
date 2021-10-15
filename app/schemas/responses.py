from typing import Optional
from pydantic.main import BaseModel


class ResponseCreate(BaseModel):
    question_id: int
    user_id: int
    choice_id: Optional[int] = None
    text: Optional[str] = None


class ResponseUpdate(BaseModel):
    choice_id: Optional[int] = None
    text: Optional[str] = None


class Response(ResponseCreate):
    id: int

    class Config:
        orm_mode = True
