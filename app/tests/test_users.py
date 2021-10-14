from tests.conftest import client


def test_post():
    response = client.post("/users/", json={
        "name": "John"
    })
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "John"
    }


def test_get_single():
    client.post("/users/", json={
        "name": "John"
    })

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "John"
    }


def test_get_all():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

    client.post("/users/", json={
        "name": "John"
    })

    client.post("/users/", json={
        "name": "Mary"
    })

    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "John"
        },
        {
            "id": 2,
            "name": "Mary"
        }
    ]


def test_patch():
    client.post("/users/", json={
        "name": "John"
    })

    response = client.patch("/users/1", json={
        "name": "Mary"
    })
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Mary"
    }


def test_delete():
    client.post("/users/", json={
        "name": "John"
    })

    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "John"
    }

    response = client.get("/users/")
    assert response.json() == []


def test_get_invalid_id():
    response = client.get("/users/1")
    assert response.status_code == 404


def test_patch_invalid_id():
    response = client.patch("/users/1", json={
        "name": "rename"
    })
    assert response.status_code == 404


def test_delete_invalid_id():
    response = client.delete("/users/1")
    assert response.status_code == 404
