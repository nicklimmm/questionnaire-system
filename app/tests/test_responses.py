from tests.conftest import client
import pytest


@pytest.fixture(autouse=True)
def setup():
    client.post("/users/", json={"name": "John"})
    client.post("/questions/",
                json={"type": "checkbox", "description": "question1"})
    client.post("/questions/",
                json={"type": "radio", "description": "question2"})
    client.post("/questions/",
                json={"type": "textbox", "description": "question3"})
    client.post("/choices/", json={"question_id": 1, "description": "choice1"})
    client.post("/choices/", json={"question_id": 2, "description": "choice2"})


def test_post_invalid_question():
    response = client.post(
        "/responses/", json={"question_id": 10, "user_id": 1, "text": "text"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Question with id of 10 not found"
    }


def test_invalid_user():
    response = client.post(
        "/responses/", json={"question_id": 1, "user_id": 10, "text": "text"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User with id of 10 not found"
    }


def test_invalid_choice():
    # Choice does not belong to the correct question
    response = client.post(
        "/responses/", json={"question_id": 2, "user_id": 1, "choice_id": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Choice with id of 1 does not belong to question with id of 2"
    }

    # Invalid choice
    response = client.post(
        "/responses/", json={"question_id": 2, "user_id": 1, "choice_id": 0})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Choice with id of 0 not found"
    }

    # Choice for text question
    response = client.post(
        "/responses/", json={"question_id": 3, "user_id": 1, "choice_id": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Choice with id of 1 does not belong to question with id of 3"
    }


def test_no_text_nor_choice():
    response = client.post(
        "/responses/", json={"question_id": 1, "user_id": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Both choice id and text cannot be null"
    }


def test_response_on_delete_cascade():
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 1})
    client.post("/responses/",
                json={"question_id": 2, "user_id": 1, "choice_id": 2})
    client.post("/responses/",
                json={"question_id": 3, "user_id": 1, "text": "text"})

    # Delete question
    client.delete("/questions/1")
    response = client.get("/responses/")
    assert response.json() == [{
        "id": 2, "question_id": 2, "user_id": 1, "choice_id": 2, "text": None
    }, {
        "id": 3, "question_id": 3, "user_id": 1, "choice_id": None, "text": "text"
    }]

    # Delete choice
    client.delete("/choices/2")
    response = client.get("/responses/")
    assert response.json() == [{
        "id": 3, "question_id": 3, "user_id": 1, "choice_id": None, "text": "text"
    }]

    # Delete user
    client.delete("/users/1")
    response = client.get("/responses/")
    assert response.json() == []
