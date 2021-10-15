from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.schema import Table
from database.session import Base


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    choice_id = Column(Integer, ForeignKey("choices.id", ondelete="CASCADE"))
    text = Column(String)

    question = relationship("Question", back_populates="responses")
    user = relationship("User", back_populates="responses")
    choice = relationship("Choice", back_populates="responses")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    responses = relationship(
        "Response", back_populates="user", cascade="all, delete", passive_deletes=True)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    # TODO Add enums
    type = Column(String, nullable=False)

    choices = relationship("Choice", back_populates="question",
                           cascade="all, delete", passive_deletes=True)
    responses = relationship(
        "Response", back_populates="question", cascade="all, delete", passive_deletes=True)


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)

    question = relationship("Question", back_populates="choices")
    responses = relationship(
        "Response", back_populates="choice", cascade="all, delete", passive_deletes=True)
