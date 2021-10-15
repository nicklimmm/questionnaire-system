from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.schema import Table
from database.session import Base

# TODO Add datetime key-attr
responses = Table(
    "responses", Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("choice_id", ForeignKey("choices.id"))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    choices = relationship("Choice", secondary=responses,
                           back_populates="users")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    # TODO Add enums
    type = Column(String, nullable=False)

    choices = relationship("Choice", back_populates="question",
                           cascade="all, delete", passive_deletes=True)


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey(
        "questions.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)

    question = relationship("Question", back_populates="choices")
    users = relationship("User", secondary=responses, back_populates="choices")
