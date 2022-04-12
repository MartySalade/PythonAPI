from fastapi.testclient import TestClient

from pythonapi import __version__


def test_version() -> int:
    assert __version__ == "0.1.0"
    return 0


def test_hello_world(client: TestClient) -> int:
    """Start with a blank database."""
    res = client.get("/")
    assert {
        "Welcome": "Please go to the /docs route to check the API documentation"
    } == res.json()
    return 0


def test_read_users(client: TestClient) -> int:
    response = client.get("/users/")
    assert response.status_code == 200
    return 0
