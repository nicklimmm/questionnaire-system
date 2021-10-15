from fastapi.encoders import jsonable_encoder
from crud.base import CRUDBase
from schemas.responses import ResponseCreate, ResponseUpdate
from database.models import Response, Question, User, Choice
from typing import Optional
from sqlalchemy.orm import Session


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]):

    def get_all(self, db: Session, question_id: int, user_id: int):
        result = db.query(self.model)
        if question_id is not None:
            result = result.filter(self.model.question_id == question_id)
        if user_id is not None:
            result = result.filter(self.model.user_id == user_id)
        return result.all()

    def create(self, db: Session, obj_in: ResponseCreate):
        obj_in_data = jsonable_encoder(obj_in)

        # If both choice_id and text are not provided
        if obj_in_data["choice_id"] is None and obj_in_data["text"] is None:
            return {
                "msg": "Both choice id and text cannot be null"
            }

        # If both choice_id and text are provided
        if obj_in_data["choice_id"] is not None and obj_in_data["text"] is not None:
            return {
                "msg": "Both choice id and text cannot be present"
            }

        question_id = obj_in_data["question_id"]
        db_question = db.query(Question).filter(
            Question.id == question_id).first()

        # If question not found
        if db_question is None:
            return {
                "msg": f"Question with id of {question_id} not found"
            }

        user_id = obj_in_data["user_id"]
        db_user = db.query(User).filter(User.id == user_id).first()

        # If user not found
        if db_user is None:
            return {
                "msg": f"User with id of {user_id} not found"
            }

        if obj_in_data["choice_id"] is not None:
            choice_id = obj_in_data["choice_id"]
            db_choice = db.query(Choice).filter(Choice.id == choice_id).first()

            # If choice not found
            if db_choice is None:
                return {
                    "msg": f"Choice with id of {choice_id} not found"
                }

            # If the choice does not belong to the question
            if db_choice.question_id != question_id:
                return {
                    "msg": f"Choice with id of {choice_id} does not belong to question with id of {question_id}"
                }

        # Checking if text is given for textbox is unnecessary, as it will give an error from the above cases

        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id: int, response: ResponseUpdate):
        db_response = db.query(self.model).filter(self.model.id == id).first()

        # Response not found
        if db_response is None:
            return None

        response_data = jsonable_encoder(response)

        # Text is provided for a non-text question
        if db_response.text is None and response_data.text is not None:
            return {
                "msg": f"Question with id of {db_response.question_id} is not of type text"
            }

        # Choice is provided for a text question
        if db_response.text is not None and response_data.choice_id is not None:
            return {
                "msg": f"Question with id of {db_response.question_id} is of type text"
            }

        if response_data.choice_id is not None:
            choice_id = response_data.choice_id
            db_choice = db.query(Choice).filter(Choice.id == choice_id).first()

            # Choice not found
            if db_choice is None:
                return {
                    "msg": f"Choice with id of {choice_id} not found"
                }

            # Choice does not belong to the question
            if db_choice.question_id != db_response.question_id:
                return {
                    "msg": f"Choice with id of {choice_id} does not belong to question with id of {db_response.question_id}"
                }

        # Only update for given fields
        for key, value in response_data.items():
            setattr(response, key, value) if value else None

        db.add(response)
        db.commit()
        db.refresh(response)
        return response


crud_responses = CRUDResponse(Response)
