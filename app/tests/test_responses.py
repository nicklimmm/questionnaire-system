from tests.conftest import client
import pytest


@pytest.fixture(autouse=True)
def setup():
    client.post("/users/", json={"name": "John"})
    client.post("/users/", json={"name": "Mary"})
    client.post("/questions/",
                json={"type": "checkbox", "description": "question1"})
    client.post("/questions/",
                json={"type": "radio", "description": "question2"})
    client.post("/questions/",
                json={"type": "textbox", "description": "question3"})
    client.post("/choices/", json={"question_id": 1, "description": "choice1"})
    client.post("/choices/", json={"question_id": 2, "description": "choice2"})
    client.post("/choices/", json={"question_id": 1, "description": "choice3"})


def test_get_with_filters():
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 1})
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 3})
    client.post("/responses/",
                json={"question_id": 1, "user_id": 2, "choice_id": 1})
    client.post("/responses/",
                json={"question_id": 2, "user_id": 2, "choice_id": 2})

    # Filter by question id
    response = client.get("/responses/?question_id=1")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 1, "text": None
    }, {
        "id": 2, "question_id": 1, "user_id": 1, "choice_id": 3, "text": None
    }, {
        "id": 3, "question_id": 1, "user_id": 2, "choice_id": 1, "text": None
    }]

    # Filter by user id
    response = client.get("/responses/?user_id=2")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 3, "question_id": 1, "user_id": 2, "choice_id": 1, "text": None
    }, {
        "id": 4, "question_id": 2, "user_id": 2, "choice_id": 2, "text": None
    }]

    # Filter by both question id and user id
    response = client.get("/responses/?question_id=1&user_id=1")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 1, "text": None
    }, {
        "id": 2, "question_id": 1, "user_id": 1, "choice_id": 3, "text": None
    }]


def test_post():
    response = client.post("/responses/",
                           json={"question_id": 1, "user_id": 1, "choice_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 1, "text": None
    }


def test_get():
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 1})

    response = client.get("/responses/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 1, "text": None
    }


def test_delete():
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 1})

    response = client.delete("/responses/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 1, "text": None
    }

    response = client.get("/responses/1")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Response with id of 1 not found"
    }


def test_patch():
    client.post("/responses/",
                json={"question_id": 1, "user_id": 1, "choice_id": 1})

    # Edit choice-based question
    response = client.patch("/responses/1", json={"choice_id": 3})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, "question_id": 1, "user_id": 1, "choice_id": 3, "text": None
    }

    client.post("/responses/",
                json={"question_id": 3, "user_id": 1, "text": "response text"})

    # Edit text
    response = client.patch("/responses/2", json={"text": "edited text"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 2, "question_id": 3, "user_id": 1, "choice_id": None, "text": "edited text"
    }


def test_post_invalid_question():
    response = client.post(
        "/responses/", json={"question_id": 10, "user_id": 1, "text": "text"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Question with id of 10 not found"
    }


def test_post_invalid_user():
    response = client.post(
        "/responses/", json={"question_id": 1, "user_id": 10, "text": "text"})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User with id of 10 not found"
    }


def test_post_invalid_choice():
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


def test_post_no_text_nor_choice():
    response = client.post(
        "/responses/", json={"question_id": 1, "user_id": 1})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Both choice id and text cannot be null"
    }


def test_post_response_on_delete_cascade():
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
