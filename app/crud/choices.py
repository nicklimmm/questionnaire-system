from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from schemas.choices import ChoiceCreate, ChoiceUpdate
from database.models import Choice, Question
from typing import Optional
from sqlalchemy.orm import Session


class CRUDChoice(CRUDBase[Choice, ChoiceCreate, ChoiceUpdate]):

    def get_all(self, db: Session, question_id: Optional[int] = None):
        if question_id is None:
            return db.query(self.model).all()
        else:
            return db.query(self.model).filter(self.model.question_id == question_id).all()

    def create(self, db: Session, obj_in: ChoiceCreate):
        obj_in_data = jsonable_encoder(obj_in)
        question_id = obj_in_data["question_id"]

        db_question = db.query(Question).filter(
            Question.id == question_id).first()

        # Prevent creation if the question does not exist
        if db_question is None:
            return {
                "msg": f"Question with id of {question_id} does not exist"
            }

        # Prevent creation if the question has a type of text
        if db_question.type == "text":
            return {
                "msg": f"The type of question with id of {question_id} is a text"
            }

        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_choices = CRUDChoice(Choice)
