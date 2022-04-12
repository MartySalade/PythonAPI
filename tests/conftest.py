from typing import Any

import pytest
from fastapi.testclient import TestClient

from pythonapi import app


@pytest.fixture
def client() -> Any:
    with TestClient(app.app) as client:
        yield client
