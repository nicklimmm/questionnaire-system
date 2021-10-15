import pytest
from fastapi.testclient import TestClient
from database.models import Question, User, Choice
from database.session import Base, get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_TESTING_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_TESTING_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def setup_db():
    db = TestingSessionLocal()
    delete_all(db)
    yield
    delete_all(db)
    db.close()


def delete_all(db):
    db.query(Choice).delete()
    db.query(Question).delete()
    # db.query(Response).delete()
    db.query(User).delete()
    db.commit()
