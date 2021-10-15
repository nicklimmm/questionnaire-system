from tests.conftest import client
import pytest


@pytest.fixture(autouse=True)
def setup():
    client.post("/questions/", json={
        "type": "radio",
        "description": "question1"
    })


def test_post():
    response = client.post("/choices/", json={
        "description": "choice1",
        "question_id": 1
    })

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "description": "choice1",
        "question_id": 1
    }


def test_get_invalid_id():
    response = client.get("/choices/1")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Choice with id of 1 not found"
    }


def test_post_invalid_question_id():
    response = client.post("/choices/", json={
        "description": "choice1",
        "question_id": 2
    })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Question with id of 2 not found"
    }


def test_choice_on_cascade_delete():
    client.post("/choices/", json={
        "description": "choice1",
        "question_id": 1
    })

    client.delete("/questions/1")

    response = client.get("/choices/")
    assert response.status_code == 200
    assert response.json() == []
