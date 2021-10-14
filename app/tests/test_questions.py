from tests.conftest import client


def test_post():
    response = client.post("/questions/", json={
        "type": "radio",
        "description": "question1"
    })
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "type": "radio",
        "description": "question1"
    }


def test_get_single():
    client.post("/questions/", json={
        "type": "radio",
        "description": "question1"
    })

    response = client.get("/questions/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "type": "radio",
        "description": "question1"
    }


def test_get_all():
    response = client.get("/questions/")
    assert response.status_code == 200
    assert response.json() == []

    client.post("/questions/", json={
        "type": "radio",
        "description": "question1"
    })

    client.post("/questions/", json={
        "type": "checkbox",
        "description": "question2"
    })

    response = client.get("/questions/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "type": "radio",
            "description": "question1"
        },
        {
            "id": 2,
            "type": "checkbox",
            "description": "question2"
        }
    ]


def test_delete():
    client.post("/questions/", json={
        "type": "radio",
        "description": "question1"
    })

    response = client.delete("/questions/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "type": "radio",
        "description": "question1"
    }

    response = client.get("/questions/")
    assert response.json() == []


def test_get_invalid_id():
    response = client.get("/questions/999")
    assert response.status_code == 404


def test_delete_invalid_id():
    response = client.get("/questions/999")
    assert response.status_code == 404


def test_post_invalid_type():
    response = client.post("/questions/", json={
        "type": "unknown",
        "description": "question1"
    })

    assert response.status_code != 200


def test_post_empty_description():
    response = client.post("/questions/", json={
        "type": "unknown",
        "description": ""
    })

    assert response.status_code != 200
