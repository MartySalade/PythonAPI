from pythonapi import __version__
from pythonapi.models import Base

from .conftest import client


def test_version() -> int:
    assert __version__ == "0.1.0"
    return 0


def test_hello_world(test_db: Base) -> int:
    res = client.get("/")
    assert {
        "Welcome": "Please go to the /docs route to check the API documentation"
    } == res.json()
    return 0


def test_read_users(test_db: Base) -> int:
    response = client.get("/users/")
    assert response.status_code == 200
    return 0


def test_create_user(test_db: Base) -> int:
    response = client.post("/users/test")
    assert response.status_code == 200
    assert response.json()["username"] == "test"
    assert response.json()["id"] == 1
    return 0


def test_read_user(test_db: Base) -> int:
    client.post("/users/test")
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "test"
    return 0


def test_read_not_existing_user(test_db: Base) -> int:
    response = client.get("/users/1")
    assert response.status_code == 400
    assert response.json()["detail"] == "User with id: 1 doesn't exist"
    return 0


def test_create_already_existing_user(test_db: Base) -> int:
    client.post("/users/test")
    response = client.post("/users/test")
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    return 0


def test_update_user(test_db: Base) -> int:
    client.post("/users/test")
    response = client.patch("/users/1&hiho")
    assert response.status_code == 200
    assert response.json()["username"] == "hiho"
    assert response.json()["id"] == 1
    return 0


def test_update_user_not_existing(test_db: Base) -> int:
    response = client.patch("/users/99&test")
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The user with id: 99 doesn't exists in the database"
    )
    return 0


def test_delete_user_not_existing(test_db: Base) -> int:
    response = client.delete("/users/99")
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "The user with id: 99 doesn't exists in the database, nothing to delete"
    )
    return 0


def test_delete_user(test_db: Base) -> int:
    client.post("/users/test")
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "test"
    assert response.json()["id"] == 1
    return 0
