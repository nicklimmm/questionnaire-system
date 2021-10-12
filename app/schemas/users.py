from pydantic.main import BaseModel
from schemas.alloptional import AllOptional


class UserCreate(BaseModel):
    name: str


class UserUpdate(UserCreate, metaclass=AllOptional):
    pass


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True
