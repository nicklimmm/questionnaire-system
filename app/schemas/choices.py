from pydantic.main import BaseModel


class ChoiceCreate(BaseModel):
    question_id: int
    description: str


class ChoiceUpdate(BaseModel):
    pass


class Choice(ChoiceCreate):
    id: int

    class Config:
        orm_mode = True
