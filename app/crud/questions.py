from sqlalchemy.orm import Session
from database import models
from database.session import NOW
from schemas import questions as schema


def get_questions(db: Session):
    return db.query(models.Question).all()


def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def add_question(db: Session, question: schema.QuestionCreate):
    db_question = models.Question(
        description=question.description,
        type=question.type
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(db: Session, question_id: int, question: schema.QuestionUpdate):
    db_question = db.query(models.Question).filter(
        models.Question.id == question_id
    ).first()

    if db_question is None:
        return None

    # Only update for given fields
    for key, value in vars(question).items():
        setattr(db_question, key, value) if value else None

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int):
    db_question = db.query(models.Question).filter(
        models.Question.id == question_id
    ).first()

    if db_question is None:
        return None

    db.delete(db_question)
    db.commit()
    db.refresh(db_question)
