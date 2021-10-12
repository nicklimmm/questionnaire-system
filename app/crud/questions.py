from crud.base import CRUDBase
from schemas.questions import QuestionCreate, QuestionUpdate
from database.models import Question


class CRUDUser(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


crud_questions = CRUDUser(Question)
